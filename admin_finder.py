import requests
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)

banner = f"""
{Fore.CYAN + Style.BRIGHT}
██████  █    ██ ███    ███ ██████  ███    ███ ██████
██   ██ ██  ██   ████  ████ ██   ██ ████  ████ ██   ██
██████  █████    ██ ████ ██ ██████  ██ ████ ██ ██████
██      ██  ██   ██  ██  ██ ██      ██  ██  ██ ██
██      ██   ██  ██      ██ ██      ██      ██ ██
{Style.RESET_ALL}
D E F 4 U L T  A D M I N  F I N D E R
"""

print(banner)

found_count = 0
lock = threading.Lock()

def scan_url(base_url, path):
    global found_count
    url = base_url.rstrip('/') + '/' + path.lstrip('/')
    try:
        res = requests.get(url, timeout=4)
        if res.status_code in (200, 301, 302, 403):
            with lock:
                found_count += 1
                print(f"{Fore.GREEN}[FOUND] {url} -> {res.status_code}")
    except:
        pass

def main():
    base_url = input("Enter Target URL (e.g. https://example.com): ").strip()
    with open("../wordlists/admin_paths.txt") as f:
        paths = [line.strip() for line in f if line.strip()]

    print(f"{Fore.BLUE}[+] Starting Fast Scan with 50 Threads...\n")
    time.sleep(1)

    threads = []
    for path in paths:
        t = threading.Thread(target=scan_url, args=(base_url, path))
        t.start()
        threads.append(t)
        while threading.active_count() > 50:
            time.sleep(0.01)

    for t in threads:
        t.join()

    print(f"{Fore.MAGENTA}[+] Scan Complete. Total Found: {found_count}")

if __name__ == "__main__":
    main()
