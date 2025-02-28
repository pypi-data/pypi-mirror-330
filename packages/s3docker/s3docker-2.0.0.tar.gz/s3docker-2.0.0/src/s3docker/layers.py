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
    
    def _get_layer_s3_key(self, layer_id):
        """Generate S3 key for a layer"""
        return f"{self.config['s3_path']}/layers/{layer_id}.tar"
    
    def _get_manifest_s3_key(self, image_name):
        """Generate S3 key for image manifest"""
        safe_name = image_name.replace(':', '_').replace('/', '_')
        return f"{self.config['s3_path']}/manifests/{safe_name}.json"
    
    def _get_cached_layer_path(self, layer_id):
        """Get path for cached layer"""
        return self.cache_dir / f"{layer_id}.tar"
    
    def _layer_exists_in_s3(self, layer_id):
        """Check if layer exists in S3"""
        try:
            self.s3_client.head_object(
                Bucket=self.config['bucket'],
                Key=self._get_layer_s3_key(layer_id)
            )
            return True
        except:
            return False
    
    def _layer_exists_in_cache(self, layer_id):
        """Check if layer exists in local cache"""
        return self._get_cached_layer_path(layer_id).exists()
    
    def extract_layers(self, image_name, temp_dir):
        """Extract layers from a Docker image"""
        p.cyan(f"🔍 Inspecting image layers for {image_name}...")
        
        # Get image details
        image = self.docker_client.images.get(image_name)
        image_id = image.id.split(':')[1]
        
        # Save image to temporary file
        temp_tar = os.path.join(temp_dir, f"{image_id}.tar")
        with open(temp_tar, 'wb') as f:
            for chunk in image.save():
                f.write(chunk)
        
        # Extract manifest and layers
        layers = []
        layer_files = {}
        
        with tarfile.open(temp_tar) as tar:
            # Extract manifest.json
            manifest_content = json.loads(tar.extractfile('manifest.json').read())
            manifest = manifest_content[0]  # Usually only one manifest
            
            # Store the config file
            config_file = manifest.get('Config')
            if config_file:
                config_data = tar.extractfile(config_file).read()
                config_json = json.loads(config_data)
                
                # Extract layer info from config
                if 'rootfs' in config_json and 'diff_ids' in config_json['rootfs']:
                    layer_diff_ids = config_json['rootfs']['diff_ids']
                    
                    # Mapping between diff_ids and layer tars
                    for layer in manifest.get('Layers', []):
                        tar_info = tar.getmember(layer)
                        layer_id = layer.split('/')[0]
                        layer_tar_path = os.path.join(temp_dir, f"{layer_id}.tar")
                        
                        with open(layer_tar_path, 'wb') as layer_file:
                            layer_file.write(tar.extractfile(tar_info).read())
                        
                        # Calculate layer hash
                        with open(layer_tar_path, 'rb') as f:
                            layer_hash = hashlib.sha256(f.read()).hexdigest()
                        
                        layers.append({
                            'id': layer_id,
                            'hash': layer_hash,
                            'size': os.path.getsize(layer_tar_path),
                            'path': layer_tar_path
                        })
        
        # Create image manifest
        image_manifest = {
            'name': image_name,
            'id': image_id,
            'layers': [layer['id'] for layer in layers],
            'config': config_file
        }
        
        manifest_path = os.path.join(temp_dir, 'image_manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(image_manifest, f)
        
        return image_manifest, layers, manifest_path
    
    def push_layers(self, image_name, temp_dir, replace=False):
        """Push image layers to S3"""
        # Extract layers
        manifest, layers, manifest_path = self.extract_layers(image_name, temp_dir)
        
        # Upload each layer (if not already in S3)
        for layer in layers:
            layer_id = layer['id']
            layer_path = layer['path']
            
            if not replace and self._layer_exists_in_s3(layer_id):
                p.yellow(f"📦 Layer {layer_id[:12]} already exists in S3, skipping...")
                continue
                
            p.cyan(f"☁️ Uploading layer {layer_id[:12]} ({(layer['size'] / (1024*1024)):.2f} MB)...")
            
            with tqdm(total=layer['size'], unit='B', unit_scale=True, 
                        desc=f"Layer {layer_id[:12]}") as pbar:
                self.s3_client.upload_file(
                    layer_path,
                    self.config['bucket'],
                    self._get_layer_s3_key(layer_id),
                    Callback=lambda bytes_transferred: pbar.update(bytes_transferred)
                )
            
            # Cache the layer locally
            os.makedirs(os.path.dirname(self._get_cached_layer_path(layer_id)), exist_ok=True)
            with open(self._get_cached_layer_path(layer_id), 'wb') as cache_file:
                with open(layer_path, 'rb') as source_file:
                    cache_file.write(source_file.read())
        
        # Upload manifest
        p.cyan(f"📄 Uploading image manifest...")
        self.s3_client.upload_file(
            manifest_path,
            self.config['bucket'],
            self._get_manifest_s3_key(image_name)
        )
        
        return {
            'manifest': manifest,
            'layers': layers
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
        
        # Download each layer
        downloaded_layers = []
        for layer_id in manifest['layers']:
            layer_path = os.path.join(temp_dir, f"{layer_id}.tar")
            layer_s3_key = self._get_layer_s3_key(layer_id)
            
            # Check if layer exists in local cache
            if self._layer_exists_in_cache(layer_id):
                p.yellow(f"🔍 Layer {layer_id[:12]} found in cache")
                # Copy from cache
                cached_layer = self._get_cached_layer_path(layer_id)
                with open(layer_path, 'wb') as dest, open(cached_layer, 'rb') as source:
                    dest.write(source.read())
            else:
                # Download from S3
                p.cyan(f"☁️ Downloading layer {layer_id[:12]}...")
                
                # Get file size for progress bar
                obj = self.s3_client.head_object(
                    Bucket=self.config['bucket'],
                    Key=layer_s3_key
                )
                file_size = obj['ContentLength']
                
                with tqdm(total=file_size, unit='B', unit_scale=True, 
                          desc=f"Layer {layer_id[:12]}") as pbar:
                    self.s3_client.download_file(
                        self.config['bucket'],
                        layer_s3_key,
                        layer_path,
                        Callback=lambda bytes_transferred: pbar.update(bytes_transferred)
                    )
                
                # Cache the layer
                os.makedirs(os.path.dirname(self._get_cached_layer_path(layer_id)), exist_ok=True)
                with open(self._get_cached_layer_path(layer_id), 'wb') as cache_file:
                    with open(layer_path, 'rb') as source_file:
                        cache_file.write(source_file.read())
            
            downloaded_layers.append({
                'id': layer_id,
                'path': layer_path
            })
        
        # Create a new image from the layers
        p.cyan("🐳 Reconstructing Docker image from layers...")
        image_tar_path = os.path.join(temp_dir, f"{manifest['id']}.tar")
        
        # Create minimal tar with manifest.json and layers
        self._create_image_tar(manifest, downloaded_layers, image_tar_path)
        
        # Load image into Docker
        with open(image_tar_path, 'rb') as f:
            self.docker_client.images.load(f)
        
        return image_name
    
    def _create_image_tar(self, manifest, layers, output_path):
        """Create a Docker image tar file from layers"""
        with tarfile.open(output_path, 'w') as tar:
            # Add each layer
            for layer in layers:
                layer_id = layer['id']
                layer_path = layer['path']
                
                # Add layer file
                tar.add(layer_path, arcname=f"{layer_id}/layer.tar")
                
                # Add empty json file for each layer
                layer_json = json.dumps({}).encode('utf-8')
                layer_json_info = tarfile.TarInfo(f"{layer_id}/json")
                layer_json_info.size = len(layer_json)
                tar.addfile(layer_json_info, fileobj=tempfile.BytesIO(layer_json))
                
                # Add version file
                version = "1.0".encode('utf-8')
                version_info = tarfile.TarInfo(f"{layer_id}/VERSION")
                version_info.size = len(version)
                tar.addfile(version_info, fileobj=tempfile.BytesIO(version))
            
            # Create manifest.json
            docker_manifest = [{
                'Config': '',  # Will be created by Docker
                'RepoTags': [manifest['name']],
                'Layers': [f"{layer_id}/layer.tar" for layer_id in manifest['layers']]
            }]
            
            manifest_content = json.dumps(docker_manifest).encode('utf-8')
            manifest_info = tarfile.TarInfo('manifest.json')
            manifest_info.size = len(manifest_content)
            tar.addfile(manifest_info, fileobj=tempfile.BytesIO(manifest_content))
