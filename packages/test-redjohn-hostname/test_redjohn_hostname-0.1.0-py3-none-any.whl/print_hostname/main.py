# print_hostname/print_hostname/main.py
import socket

def main():
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")
