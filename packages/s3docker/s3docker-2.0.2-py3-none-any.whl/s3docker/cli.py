import click
import json
from pathlib import Path
import os
import platform
from .core import S3DockerManager
import ultraprint.common as p
from halo import Halo

def load_configs():
    config_dir = Path.home() / '.s3docker'
    config_file = config_dir / 'configs.json'
    if (config_file.exists()):
        with open(config_file) as f:
            return json.load(f)
    return {}

def save_configs(configs):
    config_dir = Path.home() / '.s3docker'
    config_dir.mkdir(exist_ok=True)
    with open(config_dir / 'configs.json', 'w') as f:
        json.dump(configs, f, indent=2)

def get_default_cache_path():
    """Get the default cache path in a platform-friendly format for display"""
    default_path = Path.home() / '.s3docker' / 'layer_cache'
    return str(default_path)

@click.group()
def cli():
    """S3Docker - Manage Docker images using S3 storage"""
    pass

@cli.command()
def config():
    """Configure a new S3Docker profile"""
    configs = load_configs()
    
    p.cyan_bg("\n🔧 S3Docker Configuration Wizard")
    p.cyan("=" * 40)
    
    while True:
        name = click.prompt(
            p.yellow("\nEnter profile name (leave empty for 'default')"),
            default='default'
        )
        if name in configs:
            if not click.confirm(p.red(f"Profile '{name}' already exists. Overwrite?")):
                continue
        break
    
    config = {}
    p.green(f"\n📝 Configuring profile: {name}")
    p.blue("Enter your AWS credentials and settings:")
    config['aws_access_key_id'] = click.prompt(p.cyan("  AWS Access Key ID"))
    config['aws_secret_access_key'] = click.prompt(p.cyan("  AWS Secret Access Key"))
    config['aws_region'] = click.prompt(p.cyan("  AWS Region"), default="us-east-1")
    config['bucket'] = click.prompt(p.cyan("  S3 Bucket name"))
    config['s3_path'] = click.prompt(p.cyan("  S3 Path prefix"), default="docker-images")
    
    # Add prompt for cache directory with platform-aware path display
    p.blue("\nConfigure layer caching:")
    default_cache = get_default_cache_path()
    use_default = click.confirm(p.cyan(f"  Use default cache location ({default_cache})"), default=True)
    if not use_default:
        config['cache_dir'] = click.prompt(p.cyan("  Custom cache directory path"))
    else:
        config['cache_dir'] = None  # Will use default

    configs[name] = config
    save_configs(configs)
    p.green(f"\n✨ Configuration '{name}' saved successfully!")

@cli.command()
def configs():
    """List all available configurations"""
    configs = load_configs()
    if not configs:
        p.red("No configurations found. Create one using 's3docker config'")
        return
    
    p.cyan_bg("\n📋 Available configurations")
    p.cyan("=" * 40)
    
    for name in configs:
        config = configs[name]
        p.green(f"\n🔹 {name}:")
        p.blue(f"  Region: {config['aws_region']}")
        p.blue(f"  Bucket: {config['bucket']}")
        p.blue(f"  Path: {config['s3_path']}")
        if config.get('cache_dir'):
            p.blue(f"  Cache: {config['cache_dir']}")
        else:
            p.blue(f"  Cache: Default ({get_default_cache_path()})")

@cli.command()
@click.option('--from', 'from_', default='default', help='Configuration to use')
@click.option('--monolithic', is_flag=True, help='List images stored in monolithic format')
def list(from_, monolithic):
    """List all Docker images in S3"""
    try:
        spinner = Halo(text='Fetching images...', spinner='dots')
        spinner.start()
        
        manager = S3DockerManager(from_, use_layers=not monolithic)
        images = manager.list_images()
        
        spinner.stop()
        
        if not images:
            p.yellow(f"No images found in configuration '{from_}'")
            return
            
        p.cyan_bg(f"\n📦 Docker images in '{from_}' configuration")
        p.cyan("=" * 50)
        
        for img in images:
            size_mb = img['size'] / (1024 * 1024)
            modified = img['last_modified'].strftime('%Y-%m-%d %H:%M:%S')
            p.green(f"\n🐳 {img['name']}")
            p.blue(f"  Size: {size_mb:.1f} MB")
            p.blue(f"  Modified: {modified}")
            if 'layers' in img:
                p.blue(f"  Layers: {img['layers']}")
            
    except Exception as e:
        spinner.stop()
        p.red(f"Error: {str(e)}")

@cli.command()
@click.argument('image_name')
@click.option('--to', default='default', help='Configuration to use')
@click.option('--replace', is_flag=True, help='Replace existing image in S3')
@click.option('--temp', help='Temporary directory path for storing intermediate files')
@click.option('--timeout', default=120, help='Docker operation timeout in seconds')
@click.option('--monolithic', is_flag=True, help='Use single-file transfer instead of layer-based transfer')
@click.option('--cache-dir', help='Directory to use for layer caching')
def push(image_name, to, replace, temp, timeout, monolithic, cache_dir):
    """Push a Docker image to S3"""
    try:
        p.cyan(f"🚀 Pushing {image_name} to S3...")
        manager = S3DockerManager(to, temp_dir=temp, timeout=timeout, use_layers=not monolithic, cache_dir=cache_dir)
        manager.push(image_name, replace)
        p.green(f"✨ Successfully pushed {image_name} to S3 using '{to}' config")
    except TimeoutError as e:
        p.red(f"⏰ {str(e)}")
    except Exception as e:
        p.red(f"❌ Error: {str(e)}")

@cli.command()
@click.argument('image_name')
@click.option('--from', 'from_', default='default', help='Configuration to use')
@click.option('--temp', help='Temporary directory path for storing intermediate files')
@click.option('--timeout', default=120, help='Docker operation timeout in seconds')
@click.option('--monolithic', is_flag=True, help='Use single-file transfer instead of layer-based transfer')
@click.option('--cache-dir', help='Directory to use for layer caching')
def pull(image_name, from_, temp, timeout, monolithic, cache_dir):
    """Pull a Docker image from S3"""
    try:
        p.cyan(f"📥 Pulling {image_name} from S3...")
        manager = S3DockerManager(from_, temp_dir=temp, timeout=timeout, use_layers=not monolithic, cache_dir=cache_dir)
        manager.pull(image_name)
        p.green(f"✨ Successfully pulled {image_name} from S3 using '{from_}' config")
    except TimeoutError as e:
        p.red(f"⏰ {str(e)}")
    except Exception as e:
        p.red(f"❌ Error: {str(e)}")

@cli.command()
@click.option('--from', 'from_', default='default', help='Configuration to use')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def list_orphans(from_, output_json):
    """List orphaned layers (not referenced by any manifest)"""
    try:
        spinner = Halo(text='Searching for orphaned layers...', spinner='dots')
        spinner.start()
        
        manager = S3DockerManager(from_, use_layers=True)
        orphans = manager.find_orphaned_layers()
        
        spinner.stop()
        
        if not orphans:
            p.green("✅ No orphaned layers found.")
            return
            
        # If JSON output is requested
        if (output_json):
            output = []
            for layer in orphans:
                output.append({
                    'hash': layer['Hash'],
                    'size': layer['Size'],
                    'last_modified': layer['LastModified'].isoformat(),
                    'key': layer['Key']
                })
            print(json.dumps(output, indent=2))
            return
        
        # Otherwise, output in human-readable format
        total_size = sum(layer['Size'] for layer in orphans)
        p.cyan_bg(f"\n🗑️ Found {len(orphans)} orphaned layers")
        p.cyan(f"Total size: {total_size / (1024*1024):.2f} MB")
        p.cyan("=" * 50)
        
        for layer in orphans:
            size_mb = layer['Size'] / (1024 * 1024)
            modified = layer['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            p.yellow(f"\n📦 Layer: {layer['Hash'][:12]}")
            p.blue(f"  Size: {size_mb:.1f} MB")
            p.blue(f"  Modified: {modified}")
            
    except Exception as e:
        spinner.stop()
        p.red(f"Error: {str(e)}")

@cli.command()
@click.option('--from', 'from_', default='default', help='Configuration to use')
@click.option('--confirm', is_flag=True, help='Confirm deletion without prompting')
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
def cleanup_orphans(from_, confirm, dry_run):
    """Delete orphaned layers (not referenced by any manifest)"""
    try:
        spinner = Halo(text='Searching for orphaned layers...', spinner='dots')
        spinner.start()
        
        manager = S3DockerManager(from_, use_layers=True)
        
        if dry_run:
            orphans = manager.find_orphaned_layers()
            spinner.stop()
            
            if not orphans:
                p.green("✅ No orphaned layers found.")
                return
                
            total_size = sum(layer['Size'] for layer in orphans)
            p.cyan_bg(f"\n🗑️ Found {len(orphans)} orphaned layers")
            p.cyan(f"Total size that would be freed: {total_size / (1024*1024):.2f} MB")
            p.cyan("=" * 50)
            
            for layer in orphans:
                size_mb = layer['Size'] / (1024 * 1024)
                p.yellow(f"Would delete: {layer['Hash'][:12]} ({size_mb:.1f} MB)")
                
            p.blue("\nThis was a dry run. Use without --dry-run to actually delete orphaned layers.")
            return
        
        # If not a dry run, check for confirmation
        if not confirm:
            spinner.stop()
            if not click.confirm(p.yellow("Are you sure you want to delete all orphaned layers? This cannot be undone.")):
                p.blue("Operation cancelled.")
                return
            spinner.start()
            
        # Proceed with deletion
        deleted = manager.delete_orphaned_layers(dry_run=False)
        spinner.stop()
        
        if not deleted:
            p.green("✅ No orphaned layers found.")
            return
            
        total_size = sum(layer['Size'] for layer in deleted)
        p.green(f"✅ Successfully deleted {len(deleted)} orphaned layers")
        p.green(f"Freed up {total_size / (1024*1024):.2f} MB of storage")
        
    except Exception as e:
        spinner.stop()
        p.red(f"Error: {str(e)}")

@cli.command()
@click.argument('profile_name', required=False)
def edit_config(profile_name=None):
    """Edit an existing configuration profile"""
    configs = load_configs()
    if not configs:
        p.red("No configurations found. Create one using 's3docker config'")
        return
    
    # Let user select profile if not specified
    if profile_name is None:
        profile_names = list(configs.keys())
        
        p.cyan_bg("\n📋 Available profiles")
        p.cyan("=" * 40)
        
        for i, name in enumerate(profile_names, 1):
            p.yellow(f"{i}. {name}")
        
        while True:
            try:
                choice = click.prompt(
                    p.cyan("\nSelect profile to edit (number or name)"),
                    type=str
                )
                
                # Check if input is a number
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(profile_names):
                        profile_name = profile_names[idx]
                        break
                except ValueError:
                    # Input is not a number, treat as name
                    if choice in configs:
                        profile_name = choice
                        break
                    
                p.red("Invalid selection. Please try again.")
            except click.exceptions.Abort:
                p.blue("Operation cancelled.")
                return
    
    # Verify profile exists
    if profile_name not in configs:
        p.red(f"Profile '{profile_name}' not found")
        return
    
    config = configs[profile_name]
    p.green(f"\n✏️ Editing configuration: {profile_name}")
    
    # Show current settings
    p.cyan_bg("\nCurrent settings:")
    p.blue(f"  AWS Access Key ID: {config['aws_access_key_id']}")
    p.blue(f"  AWS Secret Access Key: {'*' * 10}...") # Mask for security
    p.blue(f"  AWS Region: {config['aws_region']}")
    p.blue(f"  S3 Bucket: {config['bucket']}")
    p.blue(f"  S3 Path prefix: {config['s3_path']}")
    
    if config.get('cache_dir'):
        p.blue(f"  Cache directory: {config['cache_dir']}")
    else:
        p.blue(f"  Cache directory: Default ({get_default_cache_path()})")
    
    # Options to edit
    fields = {
        '1': ('aws_access_key_id', "AWS Access Key ID"),
        '2': ('aws_secret_access_key', "AWS Secret Access Key"),
        '3': ('aws_region', "AWS Region"),
        '4': ('bucket', "S3 Bucket name"),
        '5': ('s3_path', "S3 Path prefix"),
        '6': ('cache_dir', "Cache directory"),
    }
    
    p.cyan_bg("\nWhat would you like to change?")
    for key, (_, label) in fields.items():
        p.yellow(f"{key}. {label}")
    p.yellow("7. All fields")
    p.yellow("8. Cancel")
    
    choice = click.prompt(
        p.cyan("\nEnter your choice"),
        type=click.Choice(['1', '2', '3', '4', '5', '6', '7', '8']),
        show_choices=False
    )
    
    if choice == '8':
        p.blue("Operation cancelled.")
        return
    
    # Edit selected field(s)
    if choice == '7':
        # Edit all fields
        p.cyan("\nEnter new values (press Enter to keep current value):")
        for field_name, field_label in fields.values():
            # Handle cache_dir specially
            if field_name == 'cache_dir':
                use_default = click.confirm(
                    p.cyan(f"  Use default cache location ({get_default_cache_path()})?"),
                    default=config.get('cache_dir') is None
                )
                if use_default:
                    config['cache_dir'] = None
                else:
                    default = config.get('cache_dir', '')
                    config['cache_dir'] = click.prompt(
                        p.cyan(f"  New {field_label}"),
                        default=default or "",
                        show_default=True,
                        type=str
                    ) or None
            else:
                # For other fields
                default = config.get(field_name, '')
                masked_default = default
                
                # Mask secret key for display
                if field_name == 'aws_secret_access_key' and default:
                    masked_default = default[:5] + '...' + default[-5:]
                
                new_value = click.prompt(
                    p.cyan(f"  New {field_label}"),
                    default=masked_default or "",
                    show_default=True,
                    type=str
                )
                
                # Only update if user entered something
                if new_value and new_value != masked_default:
                    config[field_name] = new_value
    else:
        # Edit just one field
        field_name, field_label = fields[choice]
        
        # Handle cache_dir specially
        if field_name == 'cache_dir':
            use_default = click.confirm(
                p.cyan(f"  Use default cache location ({get_default_cache_path()})?"),
                default=config.get('cache_dir') is None
            )
            if use_default:
                config['cache_dir'] = None
            else:
                default = config.get('cache_dir', '')
                config['cache_dir'] = click.prompt(
                    p.cyan(f"  New {field_label}"),
                    default=default or "",
                    show_default=True,
                    type=str
                ) or None
        else:
            # For other fields
            default = config.get(field_name, '')
            masked_default = default
            
            # Mask secret key for display
            if field_name == 'aws_secret_access_key' and default:
                masked_default = default[:5] + '...' + default[-5:]
            
            new_value = click.prompt(
                p.cyan(f"  New {field_label}"),
                default=masked_default or "",
                show_default=True,
                type=str
            )
            
            # Only update if user entered something
            if new_value and new_value != masked_default:
                config[field_name] = new_value
    
    # Save updated configuration
    configs[profile_name] = config
    save_configs(configs)
    p.green(f"\n✅ Configuration '{profile_name}' has been updated!")

if __name__ == '__main__':
    cli()
