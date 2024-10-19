#!/usr/bin/env python3

import os
import sys
import socket
import subprocess
from datetime import datetime
from urllib.request import urlretrieve

def check_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        print("\33[0;49;37mpip is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\33[0;49;37mpip is not installed. Installing pip...")
        get_pip()

def get_pip():
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = "/tmp/get-pip.py"

    try:
        print("\33[0;49;37mDownloading get-pip.py...")
        urlretrieve(get_pip_url, get_pip_path)

        print("\33[0;49;37mInstalling pip using get-pip.py...")
        subprocess.check_call(["sudo", sys.executable, get_pip_path])
        print("\33[0;49;37mpip installation was successful using get-pip.py.")

        os.remove(get_pip_path)
    except Exception as e:
        print(f"\33[0;49;37mFailed to install pip using get-pip.py. Error: ",f'\33[0;49;91m{e}')
        sys.exit(1)


def dependencies(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"\33[0;49;37m{package} has been installed successfully.")
    except subprocess.CalledProcessError:
        print(f"\33[0;49;37mNormal installation failed. Trying with --break-system-packages for {package}...")
        try:
            subprocess.check_call(["sudo", sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
            print(f"\33[0;49;37m{package} has been installed successfully using --break-system-packages.")
        except subprocess.CalledProcessError as e:
            print(f"\33[0;49;37mFailed to install {package} even with --break-system-packages. Error: ",f'\33[0;49;91m{e}')
            sys.exit(1)


try:
    import pyfiglet
except ImportError:
    print("\33[0;49;37mpyfiglet is not installed. Installing pyfiglet...")
    dependencies("pyfiglet")
    import pyfiglet

ascii_banner = pyfiglet.figlet_format("KINGCOBR@ PORT SCANNER")
print(ascii_banner)

if len(sys.argv) == 2:

    target_ip = socket.gethostbyname(sys.argv[1])
else:

    print("\33[0;49;91m Invalid Target !!")
    sys.exit()

print ("\33[0;49;37m-" * 50,f'\nstarting scan\n{datetime.now()}\nTarget: {target_ip}\n',"-" * 50,)

def TCP(target, port):
    try:
        print(f"\33[0;49;37mScanning TCP Port {port}...    ", end='\r')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)
        result = connection.connect_ex((target, port))
        if result == 0:
            print(f"\33[0;49;37mTCP Port {port} is open    ")
        connection.close()
    except Exception as e:
        print(f"\33[0;49;37mError scanning TCP port {port}: ",f'\33[0;49;91m{e}')

def UDP(target, port):
    try:
        print(f"\33[0;49;37mScanning UDP Port {port}...    ", end='\r')
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(3)
        connection.sendto(b'', (target, port))
        try:
            data, _ = connection.recvfrom(1024)
            print(f"\33[0;49;37mUDP Port {port} is open    ")
        except socket.timeout:
            print(f"\33[0;49;37mUDP Port {port} may be open    ")
        connection.close()
    except Exception as e:
        print(f"\33[0;49;37mError scanning UDP port {port}: ",f'\33[0;49;91m{e}')

try:
    for port in range(1, 1024):
        TCP(target_ip, port)
    for port in range(1, 1024):
        UDP(target_ip, port)

except KeyboardInterrupt:
    print("\n\33[0;49;37m Exiting Program.....")
    sys.exit()
except socket.gaierror:
    print("\nf'\33[0;49;91m Hostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\n f'\33[0;49;91m Server not responding !!!!")
    sys.exit()
