from setuptools import setup, find_packages

setup(
    name='quick-ssh',
    version='0.0.2',
    entry_points={
        'console_scripts': [
            'quickssh=quick_ssh.app:main'
        ]
    },
    description='Quick SSH connection manager',
    license='MIT',
    author='Shivam Bhilarkar',
    author_email='shivambhilarkar@gmail.com',
    keywords=['quick-ssh', 'ssh', 'ssh-manager'],
    url='https://github.com/shivambhilarkar',
    packages=find_packages(),  # Automatically find all packages
    install_requires=['prompt-toolkit==3.0.50', 'requests==2.32.3'],
)
