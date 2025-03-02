import os
import re
from setuptools import setup, find_packages

def get_and_update_version() -> str:
    init_file_path = os.path.join('act', '__init__.py')
    with open(init_file_path, 'r') as f:
        init_content = f.read()
    
    version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", init_content)
    if not version_match:
        raise RuntimeError("Unable to find version string.")
    
    current_version = version_match.group(1)
    
    # Split the version into its components
    version_parts = current_version.split('.')
    
    # Increment the patch version
    new_patch = int(version_parts[2]) + 1
    
    # Generate new version string
    new_version = f"{version_parts[0]}.{version_parts[1]}.{new_patch}"
    
    # Update the version in the file
    with open(init_file_path, 'w') as f:
        f.write(re.sub(r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
                       f"__version__ = '{new_version}'", init_content))
    
    print(f"Updated version from {current_version} to {new_version}")
    return new_version

def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

def clean_requires(requires):
    return [req for req in requires if not req.startswith('file://') and '@file://' not in req]

install_requires = [
    'aiohappyeyeballs==2.4.3',
    'aiohttp==3.10.10',
    'aiosignal==1.3.1',
    'annotated-types==0.7.0',
    'anyio==4.6.2.post1',
    'async-timeout==4.0.3',
    'attrs==24.2.0',
    'certifi==2024.8.30',
    'charset-normalizer==3.4.0',
    'dataclasses-json==0.6.7',
    'distro==1.9.0',
    'exceptiongroup==1.2.2',
    'frozenlist==1.4.1',
    'h11==0.14.0',
    'httpcore==1.0.6',
    'httpx==0.27.2',
    'idna==3.10',
    'jiter==0.6.1',
    'jsonpatch==1.33',
    'jsonpointer==3.0.0',
    'langchain==0.3.3',
    'langchain-community==0.3.2',
    'langchain-core==0.3.11',
    'langchain-openai==0.2.2',
    'langchain-text-splitters==0.3.0',
    'langsmith==0.1.135',
    'marshmallow==3.22.0',
    'multidict==6.1.0',
    'mypy-extensions==1.0.0',
    'numpy==1.26.4',
    'openai==1.51.2',
    'orjson==3.10.7',
    'packaging==24.1',
    'propcache==0.2.0',
    'pydantic==2.9.2',
    'pydantic-settings==2.6.0',
    'pydantic_core==2.23.4',
    'python-dotenv==1.0.1',
    'PyYAML==6.0.2',
    'regex==2024.9.11',
    'requests==2.32.3',
    'requests-toolbelt==1.0.0',
    'sniffio==1.3.1',
    'SQLAlchemy==2.0.36',
    'tenacity==8.5.0',
    'tiktoken==0.8.0',
    'tqdm==4.66.5',
    'typing-inspect==0.9.0',
    'typing_extensions==4.12.2',
    'urllib3==2.2.3',
    'yarl==1.15.4',
    'slack-sdk==3.33.1',
    'colorama>=0.4.6',
    'tabulate==0.9.0',

]

cleaned_requires = clean_requires(install_requires)
print(f"Original install_requires: {install_requires}")
print(f"Cleaned install_requires: {cleaned_requires}")

setup(
    name='act-workflow',
    version=get_and_update_version(),
    author='Taj Noah',
    author_email='mail@tajnoah.me',
    description='A library for executing workflow nodes based on Actfile configuration',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/tajalagawani/actpip',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={
        'act': ['py.typed', '*.pyi', '**/*.pyi'],
    },
    include_package_data=True,
    install_requires=cleaned_requires,
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'mypy>=0.910',
            'flake8>=3.9.2',
            
           

        ],
    },
    entry_points={
        'console_scripts': [
            'act=act.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    license='MIT',
)

print(f"Setup completed with version: {get_and_update_version()}")
