#!/usr/bin/env python3

import os
import sys
import socket
import argparse
import threading
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


parser = argparse.ArgumentParser(description="Port scanner with specified port range")
########## parser arguments ##########
parser.add_argument("target", help="The target IP address or hostname to scan")
parser.add_argument("-p", "--port", help="Port range to scan, e.g., 1-200 | For a single port scan e.g., 53-53", default="1-1024")
parser.add_argument("-t", "--tcp", action="store_true", help="Perform a TCP scan")
parser.add_argument("-u", "--udp", action="store_true", help="Perform a UDP scan")
#####################################
args = parser.parse_args()

try:
    start_port, end_port = map(int, args.port.split('-'))
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        raise ValueError
except ValueError:
    print("\33[0;49;91mInvalid port range. Please specify a valid range like 1-200.")
    sys.exit(1)

try:
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror:
    print("\33[0;49;91mInvalid target. Please provide a valid IP address or hostname.")
    sys.exit(1)


print("\33[0;49;37m-" * 50, f'\nStarting scan\n{datetime.now()}\nTarget: {target_ip}\nPort range: {start_port}-{end_port}\n', "-" * 50)

def TCP(target, port):
    try:
        print(f"\33[0;49;37mScanning TCP Port {port}...     ", end='\r')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = connection.connect_ex((target, port))
        if result == 0:
            print(f"\33[0;49;37mTCP Port {port} is open     ")
        connection.close()
    except Exception as e:
        print(f"\33[0;49;37mError scanning TCP port {port}: ",f'\33[0;49;91m{e}')

def UDP(target, port):
    try:
        print(f"\33[0;49;37mScanning UDP Port {port}...     ", end='\r')
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(0.5)
        connection.sendto(b'', (target, port))
        try:
            data, _ = connection.recvfrom(1024)
            print(f"\33[0;49;37mUDP Port {port} is open     ")
        except socket.timeout:
            pass
        connection.close()
    except Exception as e:
        print(f"\33[0;49;37mError scanning UDP port {port}: ",f'\33[0;49;91m{e}')

def thread_scan(target, start_port, end_port, scan_type):
    threads = []
    for port in range(start_port, end_port + 1):
        if scan_type == "tcp":
            thread = threading.Thread(target=TCP, args=(target, port))
        elif scan_type == "udp":
            thread = threading.Thread(target=UDP, args=(target, port))
        threads.append(thread)
        thread.start()
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

if not args.tcp and not args.udp:
    args.tcp = True
    args.udp = True

try:
    if args.tcp:
        thread_scan(target_ip, start_port, end_port, "tcp")
    if args.udp:
         thread_scan(target_ip, start_port, end_port, "udp")


except KeyboardInterrupt:
    print("\n\33[0;49;37m Exiting Program.....")
    sys.exit()
except socket.gaierror:
    print("\nf'\33[0;49;91m Hostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\n f'\33[0;49;91m Server not responding !!!!")
    sys.exit()
