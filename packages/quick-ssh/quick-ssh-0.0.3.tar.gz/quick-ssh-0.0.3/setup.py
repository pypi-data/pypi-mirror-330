from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='quick-ssh',
    version='0.0.3',
    entry_points={
        'console_scripts': [
            'quickssh=quick_ssh.app:main'
        ]
    },
    description='Quick SSH connection manager',
    long_description= long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Shivam Bhilarkar',
    author_email='shivambhilarkar@gmail.com',
    keywords=['quick-ssh', 'ssh', 'ssh-manager'],
    url='https://github.com/shivambhilarkar',
    packages=find_packages(),
    install_requires=['prompt-toolkit', 'requests'],
)
