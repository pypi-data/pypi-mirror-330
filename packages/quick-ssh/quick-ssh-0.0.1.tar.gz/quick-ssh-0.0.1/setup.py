from setuptools import setup, find_packages
from pathlib import Path


def read_md_file():
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    return long_description


setup(
    name='quick-ssh',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'quickssh=quick_ssh.app:main'
        ]
    },
    description='Quick SSH connection manager',
    long_description= read_md_file(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Shivam Bhilarkar',
    author_email='shivambhilarkar@gmail.com',
    keywords=['quick-ssh', 'ssh', 'ssh-manager'],
    url='https://github.com/shivambhilarkar',
    packages=find_packages(),
    install_requires=['prompt-toolkit', 'requests'],
)
