import socket
import threading
from datetime import datetime
from colorama import Fore, Style, init


init()
open_ports = []

def scan_port(target, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((target, port))
        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"
        result = f"[+] Port {port} is OPEN ({service})"
        print(Fore.GREEN + result + Style.RESET_ALL)
        open_ports.append((port, service))
        s.close()
    except:
        print(Fore.RED + f"[-] Port {port} is CLOSED" + Style.RESET_ALL)

def save_results(target, ports):
    with open("scan_results.txt", "w") as f:
        f.write(f"Scan Results for {target} - {datetime.now()}\n")
        f.write("-" * 40 + "\n")
        for port, service in ports:
            f.write(f"Port {port}: OPEN ({service})\n")
        f.write("-" * 40 + "\n")
    print(Fore.CYAN + f"\n[+] Results saved to scan_results.txt" + Style.RESET_ALL)

def main():
    print(Fore.YELLOW + "\n=== Python Multi-threaded Port Scanner ===\n" + Style.RESET_ALL)
    print(Fore.BLUE + "\n ====BY Hanezx1====\n" + Style.RESET_ALL)
    
    
    target = input("Enter target IP or domain: ").strip()
    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print(Fore.RED + "[!] Invalid target address." + Style.RESET_ALL)
        return

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
    except ValueError:
        print(Fore.RED + "[!] Please enter valid port numbers." + Style.RESET_ALL)
        return

    print(f"\n[~] Scanning {target} from port {start_port} to {end_port}...\n")

    start_time = datetime.now()
    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = datetime.now()
    duration = end_time - start_time

    print(Fore.BLUE + f"\n[+] Scan completed in {duration}" + Style.RESET_ALL)

    if open_ports:
        save_results(target, open_ports)
    else:
        print(Fore.YELLOW + "[!] No open ports found." + Style.RESET_ALL)

if __name__ == "__main__":
    main()