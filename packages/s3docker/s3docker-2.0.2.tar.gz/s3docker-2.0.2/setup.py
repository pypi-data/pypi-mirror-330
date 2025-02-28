from setuptools import setup, find_packages
from pathlib import Path

# Get the long description from the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='s3docker',
    version='2.0.2',
    license="MIT",
    author='Ranit Bhowmick',
    author_email='bhowmickranitking@duck.com',
    description='A tool to manage Docker images using S3 storage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kawai-Senpai/s3Docker',
    install_requires=[
        'boto3==1.34.106',
        'docker==7.1.0',
        'click==8.1.8',
        'ultraprint>=3.1.0',
        'tqdm>=4.65.0',
        'halo>=0.0.31'
    ],
    entry_points={
        'console_scripts': [
            's3docker=s3docker.cli:cli',
        ],
    },
    python_requires='>=3.6',
)
