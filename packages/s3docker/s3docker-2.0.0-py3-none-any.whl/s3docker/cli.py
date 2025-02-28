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

if __name__ == '__main__':
    cli()
