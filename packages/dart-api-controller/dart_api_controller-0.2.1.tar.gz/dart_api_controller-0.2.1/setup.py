from setuptools import setup, find_packages

setup(
    name='dart_api_controller',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'lxml>=4.9.0',
        'tqdm>=4.65.0',
        'python-dateutil>=2.8.2',
        'openai>=1.0.0',
        'boto3>=1.34.0',
        'shining-pebbles>=0.4.3',
        'canonical-transformer>=0.2.2',
        'aws-s3-controller>=0.1.0',
        'financial-dataset-preprocessor>=0.1.0',
        'beautifulsoup4>=4.12.0'
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A Python package for interacting with DART (Data Analysis, Retrieval and Transfer) API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nailen1/dart_api_controller',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.11',
)
