from setuptools import setup
import sys
import platform

system = platform.system().lower()
machine = platform.machine().lower()
binary_name = None
if system == 'linux' and 'x86_64' in machine:
    binary_name = 'ariana-linux-x64'
elif system == 'darwin':
    if 'x86_64' in machine:
        binary_name = 'ariana-macos-x64'
    elif 'arm64' in machine:
        binary_name = 'ariana-macos-arm64'
    else:
        raise Exception("Unsupported macOS architecture")
elif system == 'windows' and ('x86_64' in machine or 'amd64' in machine):
    binary_name = 'ariana-windows-x64.exe'
else:
    raise Exception("Unsupported platform or architecture")

setup(
    name='ariana',
    version='0.1.4',
    description='Ariana CLI - A tool for code instrumentalization and execution with observability',
    packages=['ariana'],
    package_data={
        'ariana': [f'bin/{binary_name}'],
    },
    entry_points={
        'console_scripts': [
            'ariana = ariana:main',
        ],
    },
    url='https://github.com/dedale-dev/ariana',
)
