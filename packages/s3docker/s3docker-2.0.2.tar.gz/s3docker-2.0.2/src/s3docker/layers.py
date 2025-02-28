import os
import json
import hashlib
import tempfile
from pathlib import Path
import tarfile
import docker
import boto3
from tqdm import tqdm
import ultraprint.common as p
import shutil
import re

class LayerManager:
    """Handles Docker image layer operations"""
    
    def __init__(self, docker_client, s3_client, config, cache_dir=None):
        self.docker_client = docker_client
        self.s3_client = s3_client
        self.config = config
        
        # Set up layer cache
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / '.s3docker' / 'layer_cache'
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_normalized_layer_id(self, layer_id):
        """Normalize a layer ID to a consistent format for comparison"""
        # Extract the hash part from the layer ID
        if layer_id.startswith("blobs/sha256/"):
            return layer_id.split("/")[-1]
        elif layer_id.startswith("sha256:"):
            return layer_id.split(":")[-1]
        return layer_id
    
    def _get_layer_s3_key(self, layer_id):
        """Generate S3 key for a layer"""
        # Normalize to hash only for storage
        hash_part = self._get_normalized_layer_id(layer_id)
        return f"{self.config['s3_path']}/layers/sha256/{hash_part}.tar"
    
    def _get_manifest_s3_key(self, image_name):
        """Generate S3 key for image manifest"""
        safe_name = image_name.replace(':', '_').replace('/', '_')
        return f"{self.config['s3_path']}/manifests/{safe_name}.json"
    
    def _get_cached_layer_path(self, layer_id):
        """Get path for cached layer"""
        # Normalize to hash only for storage
        hash_part = self._get_normalized_layer_id(layer_id)
        return self.cache_dir / f"sha256_{hash_part}.tar"
    
    def _layer_exists_in_s3(self, layer_id):
        """Check if layer exists in S3"""
        try:
            s3_key = self._get_layer_s3_key(layer_id)
            p.blue(f"Checking if layer exists: {s3_key}")
            self.s3_client.head_object(
                Bucket=self.config['bucket'],
                Key=s3_key
            )
            return True
        except Exception as e:
            if "404" in str(e):
                return False
            # For other errors, log and treat as not existing
            p.yellow(f"Error checking layer existence: {str(e)}")
            return False
    
    def _layer_exists_in_cache(self, layer_id):
        """Check if layer exists in local cache"""
        return self._get_cached_layer_path(layer_id).exists()
    
    def extract_layers(self, image_name, temp_dir):
        """Extract layers from a Docker image"""
        p.cyan(f"🔍 Inspecting image layers for {image_name}...")
        
        # Get image details
        image = self.docker_client.images.get(image_name)
        image_id = image.id.split(':')[1] if ':' in image.id else image.id
        
        # Save image to temporary file
        temp_tar = os.path.join(temp_dir, f"{image_id}.tar")
        with open(temp_tar, 'wb') as f:
            for chunk in image.save():
                f.write(chunk)
        
        p.cyan(f"📦 Extracting layers from image...")
        
        # Extract tar to a directory for easier handling
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        with tarfile.open(temp_tar) as tar:
            tar.extractall(extract_dir)
        
        # Read manifest.json
        with open(os.path.join(extract_dir, "manifest.json")) as f:
            manifest_content = json.loads(f.read())
            manifest = manifest_content[0]  # Usually only one manifest
        
        # Get config file content
        config_file = manifest.get('Config')
        config_path = os.path.join(extract_dir, config_file) if config_file else None
        
        # Process layers
        layers = []
        for layer_path in manifest.get('Layers', []):
            full_layer_path = os.path.join(extract_dir, layer_path)
            
            # Layer ID is the full reference as in manifest
            layer_id = layer_path
            
            # Get layer size
            layer_size = os.path.getsize(full_layer_path)
            
            # Calculate hash (optional, as we already have the hash in the path)
            layer_hash = layer_path.split('/')[-1] if '/' in layer_path else layer_path
            
            layers.append({
                'id': layer_id,
                'hash': layer_hash,
                'size': layer_size,
                'path': full_layer_path
            })
        
        # Create image manifest
        image_manifest = {
            'name': image_name,
            'id': image_id,
            'layers': [layer['id'] for layer in layers],
            'config': config_file
        }
        
        # Save the manifest
        manifest_path = os.path.join(temp_dir, 'image_manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(image_manifest, f)
        
        p.cyan(f"📝 Extracted {len(layers)} layers")
        
        # Save the original manifest and other files for potential use during reconstruction
        shutil.copy(
            os.path.join(extract_dir, "manifest.json"),
            os.path.join(temp_dir, "original_manifest.json")
        )
        
        # Copy config file if it exists
        if config_file and os.path.exists(os.path.join(extract_dir, config_file)):
            # Create directory structure if needed
            os.makedirs(os.path.dirname(os.path.join(temp_dir, config_file)), exist_ok=True)
            shutil.copy(
                os.path.join(extract_dir, config_file),
                os.path.join(temp_dir, config_file)
            )
        
        return image_manifest, layers, manifest_path
    
    def push_layers(self, image_name, temp_dir, replace=False):
        """Push image layers to S3"""
        # Extract layers
        manifest, layers, manifest_path = self.extract_layers(image_name, temp_dir)
        
        # Track which layers were uploaded and which were skipped
        uploaded_layers = []
        skipped_layers = []
        
        # Also upload config file if available
        config_file = manifest.get('config')
        if config_file:
            config_path = os.path.join(temp_dir, config_file)
            if os.path.exists(config_path):
                config_key = f"{self.config['s3_path']}/{config_file}"
                
                # Check if config already exists
                config_exists = False
                if not replace:
                    try:
                        self.s3_client.head_object(
                            Bucket=self.config['bucket'],
                            Key=config_key
                        )
                        config_exists = True
                        p.yellow(f"📄 Config file already exists, skipping...")
                    except:
                        pass
                
                if replace or not config_exists:
                    p.cyan(f"📄 Uploading config file...")
                    self.s3_client.upload_file(
                        config_path,
                        self.config['bucket'],
                        config_key
                    )
        
        # Upload each layer
        for layer in layers:
            layer_id = layer['id']
            layer_path = layer['path']
            layer_size = layer['size']
            
            # Skip upload if layer exists and not replacing
            if not replace and self._layer_exists_in_s3(layer_id):
                p.yellow(f"📦 Layer {layer_id.split('/')[-1][:12]} already exists in S3, skipping...")
                skipped_layers.append(layer)
                continue
                
            p.cyan(f"☁️ Uploading layer {layer_id.split('/')[-1][:12]} ({(layer_size / (1024*1024)):.2f} MB)...")
            
            with tqdm(total=layer_size, unit='B', unit_scale=True, 
                     desc=f"Layer {layer_id.split('/')[-1][:12]}") as pbar:
                self.s3_client.upload_file(
                    layer_path,
                    self.config['bucket'],
                    self._get_layer_s3_key(layer_id),
                    Callback=lambda bytes_transferred: pbar.update(bytes_transferred)
                )
            
            # Cache the layer locally
            cache_path = self._get_cached_layer_path(layer_id)
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, 'wb') as cache_file:
                with open(layer_path, 'rb') as source_file:
                    cache_file.write(source_file.read())
            
            uploaded_layers.append(layer)
        
        # Upload manifest
        p.cyan(f"📄 Uploading image manifest...")
        self.s3_client.upload_file(
            manifest_path,
            self.config['bucket'],
            self._get_manifest_s3_key(image_name)
        )
        
        # Also upload original manifest for reference
        original_manifest_path = os.path.join(temp_dir, "original_manifest.json")
        if os.path.exists(original_manifest_path):
            self.s3_client.upload_file(
                original_manifest_path,
                self.config['bucket'],
                f"{self.config['s3_path']}/original_manifests/{image_name.replace(':', '_').replace('/', '_')}.json"
            )
        
        # Print summary
        p.green(f"✅ Summary: {len(uploaded_layers)} layers uploaded, {len(skipped_layers)} layers skipped (already existed)")
        
        return {
            'manifest': manifest,
            'uploaded_layers': uploaded_layers,
            'skipped_layers': skipped_layers
        }
    
    def pull_layers(self, image_name, temp_dir):
        """Pull image layers from S3 and build image"""
        # Download manifest
        manifest_key = self._get_manifest_s3_key(image_name)
        manifest_path = os.path.join(temp_dir, 'image_manifest.json')
        
        try:
            p.cyan("📄 Downloading image manifest...")
            self.s3_client.download_file(
                self.config['bucket'],
                manifest_key,
                manifest_path
            )
        except Exception as e:
            raise FileNotFoundError(f"Image {image_name} not found in S3: {str(e)}")
        
        # Read manifest
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Create image structure
        p.cyan("🔧 Creating image directory structure...")
        
        # Directory to store the reconstructed image
        image_temp = os.path.join(temp_dir, "image")
        os.makedirs(image_temp, exist_ok=True)
        
        # Download each layer
        downloaded_layers = []
        for layer_id in manifest['layers']:
            # Create directory structure for this layer (e.g., blobs/sha256/)
            layer_dir = os.path.join(image_temp, os.path.dirname(layer_id))
            os.makedirs(layer_dir, exist_ok=True)
            
            # Target path for the layer
            layer_path = os.path.join(image_temp, layer_id)
            layer_s3_key = self._get_layer_s3_key(layer_id)
            
            # Check if layer exists in local cache
            if self._layer_exists_in_cache(layer_id):
                p.yellow(f"🔍 Layer {layer_id.split('/')[-1][:12]} found in cache")
                # Copy from cache
                cached_layer = self._get_cached_layer_path(layer_id)
                with open(layer_path, 'wb') as dest, open(cached_layer, 'rb') as source:
                    dest.write(source.read())
            else:
                # Download from S3
                p.cyan(f"☁️ Downloading layer {layer_id.split('/')[-1][:12]}...")
                
                try:
                    # Get file size for progress bar
                    obj = self.s3_client.head_object(
                        Bucket=self.config['bucket'],
                        Key=layer_s3_key
                    )
                    file_size = obj['ContentLength']
                    
                    with tqdm(total=file_size, unit='B', unit_scale=True, 
                              desc=f"Layer {layer_id.split('/')[-1][:12]}") as pbar:
                        self.s3_client.download_file(
                            self.config['bucket'],
                            layer_s3_key,
                            layer_path,
                            Callback=lambda bytes_transferred: pbar.update(bytes_transferred)
                        )
                    
                    # Cache the layer
                    cache_path = self._get_cached_layer_path(layer_id)
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    with open(cache_path, 'wb') as cache_file:
                        with open(layer_path, 'rb') as source_file:
                            cache_file.write(source_file.read())
                except Exception as e:
                    p.red(f"Error downloading layer {layer_id}: {str(e)}")
                    raise
            
            downloaded_layers.append(layer_id)
        
        # Download config file if specified in manifest
        config_file = manifest.get('config')
        if config_file:
            config_key = f"{self.config['s3_path']}/{config_file}"
            config_path = os.path.join(image_temp, config_file)
            
            # Create directory structure for config file
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            try:
                p.cyan(f"📄 Downloading image config...")
                self.s3_client.download_file(
                    self.config['bucket'],
                    config_key,
                    config_path
                )
            except:
                p.yellow("Warning: Could not download config file, will create minimal one")
                # Create minimal config file
                with open(config_path, 'w') as f:
                    f.write("{}")
        
        # Create manifest.json for Docker
        docker_manifest = [{
            'Config': config_file,
            'RepoTags': [manifest['name']],
            'Layers': downloaded_layers
        }]
        
        with open(os.path.join(image_temp, "manifest.json"), 'w') as f:
            json.dump(docker_manifest, f)
        
        # Create tar file from the image directory
        output_tar = os.path.join(temp_dir, f"{manifest['id']}.tar")
        p.cyan("📦 Creating final image archive...")
        
        with tarfile.open(output_tar, 'w') as tar:
            for root, dirs, files in os.walk(image_temp):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, image_temp)
                    tar.add(file_path, arcname=arcname)
        
        # Load image into Docker
        p.cyan("🐳 Loading image into Docker...")
        with open(output_tar, 'rb') as f:
            self.docker_client.images.load(f)
        
        return image_name
    
    def find_orphaned_layers(self):
        """Find layers that are not referenced by any manifest"""
        # Get all layers in S3
        p.cyan("📊 Listing all layers in S3...")
        all_layers = self._list_all_layers()
        
        # Get all manifests in S3
        p.cyan("📄 Listing all manifests in S3...")
        manifests = self._list_all_manifests()
        
        # Get all referenced layers
        referenced_layers = set()
        for manifest in manifests:
            try:
                # Get the manifest content
                manifest_obj = self.s3_client.get_object(
                    Bucket=self.config['bucket'],
                    Key=manifest['Key']
                )
                manifest_data = json.loads(manifest_obj['Body'].read().decode('utf-8'))
                
                # Add all layers from this manifest to the referenced set
                for layer_id in manifest_data.get('layers', []):
                    # Normalize the layer ID for comparison
                    normalized_id = self._get_normalized_layer_id(layer_id)
                    referenced_layers.add(normalized_id)
            except Exception as e:
                p.yellow(f"Error processing manifest {manifest['Key']}: {str(e)}")
                continue
        
        # Find orphaned layers (in all_layers but not in referenced_layers)
        orphaned_layers = []
        for layer in all_layers:
            # Extract the hash part from the S3 key
            match = re.search(r'/sha256/([^/]+)\.tar$', layer['Key'])
            if match:
                layer_hash = match.group(1)
                if layer_hash not in referenced_layers:
                    orphaned_layers.append({
                        'Key': layer['Key'],
                        'Size': layer['Size'],
                        'LastModified': layer['LastModified'],
                        'Hash': layer_hash
                    })
        
        return orphaned_layers
    
    def delete_orphaned_layers(self, dry_run=True):
        """Delete orphaned layers from S3"""
        orphaned_layers = self.find_orphaned_layers()
        
        if not orphaned_layers:
            p.green("✅ No orphaned layers found.")
            return []
        
        p.cyan(f"🗑️ Found {len(orphaned_layers)} orphaned layers.")
        
        deleted = []
        total_size = sum(layer['Size'] for layer in orphaned_layers)
        
        p.yellow(f"This will free approximately {total_size / (1024*1024):.2f} MB of storage.")
        
        if dry_run:
            p.blue("DRY RUN: No layers will be deleted.")
            return orphaned_layers
        
        for layer in orphaned_layers:
            try:
                p.yellow(f"Deleting layer: {layer['Hash'][:12]}")
                self.s3_client.delete_object(
                    Bucket=self.config['bucket'],
                    Key=layer['Key']
                )
                deleted.append(layer)
            except Exception as e:
                p.red(f"Error deleting layer {layer['Hash'][:12]}: {str(e)}")
        
        p.green(f"✅ Deleted {len(deleted)} orphaned layers.")
        return deleted
    
    def _list_all_layers(self):
        """List all layers in S3"""
        layers = []
        prefix = f"{self.config['s3_path']}/layers/"
        
        # Use pagination to handle large numbers of objects
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.config['bucket'], Prefix=prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.tar'):
                        layers.append(obj)
        
        return layers
    
    def _list_all_manifests(self):
        """List all manifests in S3"""
        manifests = []
        prefix = f"{self.config['s3_path']}/manifests/"
        
        # Use pagination to handle large numbers of objects
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.config['bucket'], Prefix=prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.json'):
                        manifests.append(obj)
        
        return manifests
