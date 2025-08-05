import socket
import threading
import ipaddress
from datetime import datetime
from colorama import Fore, Style, init



init()
lock = threading.Lock()
open_hosts = []

def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"
        with lock:
            print(Fore.GREEN + f"[+] {ip}:{port} OPEN ({service})" + Style.RESET_ALL)
            open_hosts.append((ip, port, service))
        s.close()
    except:
        pass

def scan_host(ip, ports):
    for port in ports:
        scan_port(str(ip), port)

def save_results():
    with open("network_scan_results.txt", "w") as f:
        f.write(f"Network Scan Results - {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        for ip, port, service in open_hosts:
            f.write(f"{ip}:{port} - {service}\n")
    print(Fore.CYAN + "\n[+] Results saved to network_scan_results.txt" + Style.RESET_ALL)

def main():
    print(Fore.YELLOW + "\n=== Network IP Range Port Scanner ===\n" + Style.RESET_ALL)
    print(Fore.BLUE + "\n =====BY Hanezx1====\n" + Style.RESET_ALL)
    
    subnet = input("Enter IP range (e.g. 192.168.1.0/24): ").strip()
    try:
        ip_net = ipaddress.ip_network(subnet, strict=False)
    except ValueError:
        print(Fore.RED + "[!] Invalid IP range." + Style.RESET_ALL)
        return

    try:
        ports_input = input("Enter ports to scan (e.g. 22,80,443): ")
        ports = [int(p.strip()) for p in ports_input.split(',')]
    except ValueError:
        print(Fore.RED + "[!] Invalid ports." + Style.RESET_ALL)
        return

    print(f"\n[~] Scanning {subnet} on ports {ports}...\n")
    start_time = datetime.now()

    threads = []
    for ip in ip_net.hosts():
        t = threading.Thread(target=scan_host, args=(ip, ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = datetime.now() - start_time
    print(Fore.BLUE + f"\n[+] Scan completed in {duration}" + Style.RESET_ALL)

    if open_hosts:
        save_results()
    else:
        print(Fore.YELLOW + "[!] No open ports found in the range." + Style.RESET_ALL)

if __name__ == "__main__":
    main()