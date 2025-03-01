import os
import subprocess
import sys
import platform

def main():
    module_dir = os.path.dirname(__file__)
    binary_dir = os.path.join(module_dir, 'bin')
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == 'linux' and 'x86_64' in machine:
        binary = os.path.join(binary_dir, 'ariana-linux-x64')
    elif system == 'darwin':
        if 'x86_64' in machine:
            binary = os.path.join(binary_dir, 'ariana-macos-x64')
        elif 'arm64' in machine:
            binary = os.path.join(binary_dir, 'ariana-macos-arm64')
        else:
            print("Unsupported macOS architecture")
            sys.exit(1)
    elif system == 'windows' and ('x86_64' in machine or 'amd64' in machine):
        binary = os.path.join(binary_dir, 'ariana-windows-x64.exe')
    else:
        print("Unsupported platform or architecture")
        sys.exit(1)

    if system in ['linux', 'darwin']:
        os.chmod(binary, 0o755)

    try:
        subprocess.run([binary] + sys.argv[1:], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running ariana: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
