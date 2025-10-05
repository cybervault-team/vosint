#!/usr/bin/env python3
import os
import threading
import requests
import json
import random
import time
from queue import Queue
import argparse

# -------------------- ASCII Art --------------------
ascii_art = r"""
__     __        _       _   
\ \   / /__  ___(_)_ __ | |_ 
 \ \ / / _ \/ __| | '_ \| __|
  \ V / (_) \__ \ | | | | |_ 
   \_/ \___/|___/_|_| |_|\__|
"""

# -------------------- Colors --------------------
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"

# -------------------- Headers --------------------
HEADERS_LIST = [
    # Firefox - Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8,de;q=0.7,fr;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com/",
    },
    # Safari - Mac
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Referer": "https://duckduckgo.com/",
    },
    # Chrome - Linux
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8,de;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Referer": "https://www.bing.com/",
    },
    # Safari - iOS
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Referer": "https://www.ecosia.org/",
    },
    # Chrome - Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Referer": "https://www.yandex.com/",
    },
    # Edge - Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Referer": "https://www.google.com/",
    },
    # Android - Chrome
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Referer": "https://duckduckgo.com/",
    }
]


# -------------------- Load Platforms --------------------
PLATFORMS = {}
try:
    with open("data/data.json", "r", encoding="utf-8") as f:
        PLATFORMS = json.load(f)
    print(f"{GREEN}[+] Loaded {len(PLATFORMS)} platforms from data.json{RESET}")
except Exception as e:
    print(f"{RED}[ERROR] Could not load platforms from data.json: {e}{RESET}")
    exit(1)
    
# -------------------- İnfo -----------------------------
def print_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BLUE + ascii_art + RESET)
    
    info_text = f"""
{GREEN}Vosint OSINT Tool - Information{RESET}

{YELLOW}Description:{RESET}
Vosint is a powerful OSINT tool designed to search for usernames across social media and web platforms.

{YELLOW}Features:{RESET}
- Search across 300+ social and web platforms
- Proxy rotation support (-p)
- Randomized User-Agent headers
- Multi-threading support (-t1 – -t5)
- Export results in JSON, TXT, and HTML formats
- Works in both CLI and interactive mode
- Live output display
- Beautiful dark-themed HTML report

{YELLOW}Purpose:{RESET}
Vosint is built for ethical OSINT investigations, digital footprint analysis, and cybersecurity education.  
The developer is not responsible for any misuse or illegal activity.

{GREEN}Developer: Coderianx – CyberVault{RESET}
© 2025.
"""
    print(info_text)


# -------------------- Proxy helpers --------------------
def load_proxies_file(path="data/proxies.json"):
    """
    Load proxies from proxies.json (top-level list or {"proxies": [...]})
    Returns a list of proxy strings.
    """
    proxies = []
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Accept either list at top-level or {"proxies": [...]}
            if isinstance(data, list):
                raw = data
            elif isinstance(data, dict) and "proxies" in data:
                raw = data["proxies"]
            else:
                raw = []
            for p in raw:
                if isinstance(p, str):
                    s = p.strip()
                    if s and not s.startswith("#"):
                        proxies.append(s)
    except Exception as e:
        print(f"{YELLOW}[!] Could not load proxies from '{path}': {e}{RESET}")
    return proxies

def build_requests_proxies(proxy_string):
    """Turn a single proxy string into requests' proxies dict."""
    if not proxy_string:
        return None
    return {"http": proxy_string, "https": proxy_string}


# -------------------- Functions --------------------
def check(platform, url, results, proxies_pool=None, retry=3, timeout=8, lock=None):
    """
    Perform GET request. If proxies_pool is provided, choose a random proxy for each attempt.
    Append found results (200/301/302) to results list (thread-safe with lock).
    """
    for attempt in range(1, retry + 1):
        try:
            proxies = None
            if proxies_pool:
                proxy_choice = random.choice(proxies_pool)
                proxies = build_requests_proxies(proxy_choice)
                
            headers = random.choice(HEADERS_LIST)
            resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
            if resp.status_code in [200, 301, 302]:
                line = f"{GREEN}[+]{RESET} {platform}: {url}"
                print(line)
                if lock:
                    with lock:
                        results.append({"platform": platform, "url": url})
                else:
                    results.append({"platform": platform, "url": url})
            # stop retrying after first real response (success or non-exception)
            break
        except requests.exceptions.RequestException:
            # failed attempt
            if attempt < retry:
                time.sleep(0.4)
                continue
            else:
                # final failure: skip silently (can be logged if desired)
                break

def thread_worker(queue, results, proxies_pool, lock):
    while True:
        try:
            platform, url = queue.get(block=False)
        except Exception:
            break
        check(platform, url, results, proxies_pool=proxies_pool, lock=lock)
        queue.task_done()

def scan(username, speed, results, proxies_pool=None):
    """
    Build queue from PLATFORMS and run worker threads.
    speed = number of threads
    proxies_pool = list of proxy strings or None
    """
    q = Queue()
    for platform, pattern in PLATFORMS.items():
        url = pattern.replace("{}", username)
        q.put((platform, url))

    threads = []
    lock = threading.Lock()
    for _ in range(max(1, speed)):
        t = threading.Thread(target=thread_worker, args=(q, results, proxies_pool, lock))
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()
    for t in threads:
        t.join(timeout=0.1)

# -------------------- Save functions --------------------
def save_txt(filename, results):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"{result['platform']}: {result['url']}\n")
        print(f"{GREEN}[+] Results saved to '{filename}'.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Could not save TXT file: {e}{RESET}")

def save_json(filename, results):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"{GREEN}[+] Results saved to '{filename}' (JSON).{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Could not save JSON file: {e}{RESET}")


def save_html(filename, results, username=None):
    try:
        total = len(PLATFORMS)
        found = len(results)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Vosint Results for {username}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
  body {{
    background: radial-gradient(circle at top left, #0d0d0d, #000);
    color: #eaeaea;
    font-family: 'Share Tech Mono', monospace;
    margin: 0;
    padding: 0;
  }}
  .container {{
    max-width: 1000px;
    margin: 40px auto;
    padding: 20px;
    text-align: center;
  }}
  h1 {{
    color: #00ff99;
    font-size: 2.2rem;
    text-shadow: 0 0 8px #00ff99, 0 0 16px #00ff99;
    margin-bottom: 10px;
  }}
  .meta {{
    color: #999;
    margin-bottom: 25px;
  }}
  .search-box {{
    margin-bottom: 25px;
  }}
  input[type="text"] {{
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    width: 70%;
    max-width: 400px;
    background: #111;
    color: #00ffcc;
    font-size: 1rem;
    outline: none;
    box-shadow: 0 0 8px rgba(0,255,204,0.3);
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
  }}
  .card {{
    background: #0f0f0f;
    border: 1px solid rgba(0,255,153,0.2);
    border-radius: 10px;
    padding: 15px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    box-shadow: 0 0 8px rgba(0,255,153,0.2);
  }}
  .card:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,255,153,0.6);
  }}
  .platform {{
    font-weight: bold;
    color: #00ffcc;
    margin-bottom: 8px;
    font-size: 1.1rem;
  }}
  .url a {{
    color: #7be495;
    text-decoration: none;
    word-break: break-all;
  }}
  .url a:hover {{
    color: #00ff99;
    text-shadow: 0 0 5px #00ff99;
  }}
  .footer {{
    margin-top: 40px;
    font-size: 0.9rem;
    color: #777;
  }}
  .stats {{
    font-size: 1rem;
    color: #00ffaa;
    margin-bottom: 20px;
  }}
</style>
</head>
<body>
<div class="container">
  <h1>Vosint OSINT Report</h1>
  <div class="meta">Target: <strong>{username}</strong></div>
  <div class="stats">✅ Found {found} of {total} platforms</div>

  <div class="search-box">
    <input type="text" id="searchInput" placeholder="Search platform or URL..." onkeyup="filterResults()">
  </div>

  <div class="grid" id="resultsGrid">
""")

            for result in results:
                f.write(f"""    <div class="card">
      <div class="platform">{result['platform']}</div>
      <div class="url"><a href="{result['url']}" target="_blank" rel="noopener noreferrer">{result['url']}</a></div>
    </div>\n""")

            f.write("""
  </div>
  <div class="footer">Generated by <span style="color:#00ffaa;">Vosint</span> • Powered by Coderianx</div>
</div>

<script>
function filterResults() {
  var input = document.getElementById('searchInput');
  var filter = input.value.toLowerCase();
  var cards = document.getElementsByClassName('card');
  for (var i = 0; i < cards.length; i++) {
    var text = cards[i].textContent.toLowerCase();
    cards[i].style.display = text.includes(filter) ? '' : 'none';
  }
}
</script>
</body>
</html>
""")
        print(f"{GREEN}[+] Results saved to '{filename}' (HTML).{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Could not save HTML file: {e}{RESET}")


# -------------------- Run Scan wrapper --------------------
def run_scan(username, speed, use_proxy=False, proxies_file="data/proxies.json", txt_filename=None, json_filename=None, html_filename=None):
    # load proxies if requested
    proxies_pool = []
    if use_proxy:
        proxies_pool = load_proxies_file(proxies_file)
        if not proxies_pool:
            print(f"{YELLOW}[!] Proxy flag set but no proxies found in '{proxies_file}'. Continuing without proxies.{RESET}")
            proxies_pool = None
        else:
            print(f"{GREEN}[+] Loaded {len(proxies_pool)} proxies from '{proxies_file}'.{RESET}")
    else:
        proxies_pool = None

    results = []
    print(BLUE + ascii_art + RESET)
    print(f"{YELLOW}[i] Starting OSINT scan for {username}. (Threads: {speed}){RESET}\n")
    scan(username, speed, results, proxies_pool=proxies_pool)

    if txt_filename:
        save_txt(txt_filename, results)
    if json_filename:
        save_json(json_filename, results)
    if html_filename:
        save_html(html_filename, results, username)

# -------------------- Argparse --------------------
parser = argparse.ArgumentParser(description="Vosint OSINT Scanner")
parser.add_argument("-u", help="Username to scan")
parser.add_argument("-t1", action="store_true", help="Speed 100")
parser.add_argument("-t2", action="store_true", help="Speed 75")
parser.add_argument("-t3", action="store_true", help="Speed 50")
parser.add_argument("-t4", action="store_true", help="Speed 25")
parser.add_argument("-t5", action="store_true", help="Speed 5")
parser.add_argument("-oN", help="Save results as TXT")
parser.add_argument("-j", help="Save results as JSON")
parser.add_argument("-h", help="Save results as HTML (not -h)")
# NEW: proxy flag: if set, load proxies from proxies.txt (or you can change path below)
parser.add_argument("-p", "--proxy", action="store_true", help="Use automatic proxy rotation from 'proxies.json' (one proxy per line)")
args = parser.parse_args()

# Determine speed (threads)
if args.t1:
    speed = 100
elif args.t2:
    speed = 75
elif args.t3:
    speed = 50
elif args.t4:
    speed = 25
elif args.t5:
    speed = 5
else:
    speed = 10

# -------------------- Run Argparse Mode --------------------
if args.u:
    run_scan(args.u, speed, use_proxy=args.proxy, proxies_file="data/proxies.json", txt_filename=args.oN, json_filename=args.j, html_filename=args.hfile)
else:
    # -------------------- Interactive Mode --------------------
    options = "[options]:\nvosint : start vosint\n-u : enter username\n-t1 : speed(100)\n-t2 : speed(75)\n-t3 : speed(50)\n-t4 : speed(25)\n-t5 : speed(5)\n-oN : save TXT\n-j : save JSON\n-h : save HTML\n-p : use automatic proxies from 'proxies.json'\n-off : exit\nclear : clear screen"
    example = "[example]: vosint -u example -t1 -oN save.txt -j save.json -hfile save.html -p"
    developed = "Developed by Coderianx - CyberVault"

    print(BLUE + ascii_art + RESET)
    print(f"{RED}{developed}{RESET}\n")
    print(f"{BLUE}{options}\n")
    print(f"{RED}Help Menu = help\n")

    while True:
        try:
            command = input(YELLOW + "$ >> " + RESET).strip()
            if not command:
                continue
            if command.lower() == 'help':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(BLUE + ascii_art + RESET)
                print(f"{BLUE}Help Menu{RESET}\n{options}\n\n{example}\n")
                continue
            if command.lower() in ["-off", "exit"]:
                print(f"{YELLOW}[!] Exiting program...{RESET}")
                break
            if command.lower() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(BLUE + ascii_art + RESET)
                print(f"{RED}{developed}{RESET}\n")
                print(f"{BLUE}{options}\n")
                continue
            if command.lower() == "info":
                print_info()
                continue

            parts = command.split()
            if not parts or parts[0].lower() != "vosint":
                print(f"{RED}[ERROR] Command must start with 'vosint'.{RESET}")
                continue

            username = None
            txt_filename = None
            json_filename = None
            html_filename = None
            use_proxy = False

            if "-u" in parts:
                i = parts.index("-u")
                if i + 1 < len(parts):
                    username = parts[i + 1]
            if not username:
                print(f"{RED}[!] Please enter a username.{RESET}")
                continue

            if "-oN" in parts:
                i = parts.index("-oN")
                if i + 1 < len(parts):
                    txt_filename = parts[i + 1]
            if "-j" in parts:
                i = parts.index("-j")
                if i + 1 < len(parts):
                    json_filename = parts[i + 1]
            if "-h" in parts:
                i = parts.index("-h")
                if i + 1 < len(parts):
                    html_filename = parts[i + 1]

            if "-p" in parts:
                use_proxy = True

            # map t flags to thread counts (you used slightly different mapping earlier; keeping simple)
            if "-t1" in parts:
                speed = 100
            elif "-t2" in parts:
                speed = 75
            elif "-t3" in parts:
                speed = 50
            elif "-t4" in parts:
                speed = 25
            elif "-t5" in parts:
                speed = 5
            else:
                speed = 10

            run_scan(username, speed, use_proxy=use_proxy, proxies_file="proxies.txt", txt_filename=txt_filename, json_filename=json_filename, html_filename=html_filename)

        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] CTRL+C detected. Exiting program...{RESET}")
            break