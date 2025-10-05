# ⚡ Vosint – Advanced OSINT Username Scanner

Vosint is a **powerful open-source OSINT tool** that searches for a given username across **300+ social media and web platforms**.  
It’s built for **ethical hackers, investigators, and cybersecurity researchers** who need to identify digital footprints quickly.

---

## 🚀 Features

- 🔍 Search usernames across 300+ platforms  
- ⚡ Multi-threaded scanning (`-t1` → `-t5` speed levels)  
- 🧩 Proxy support 
- 🧠 Randomized User-Agent headers for stealth  
- 📊 Export results in **JSON**, **TXT**, and **HTML**  
- 🌐 Beautiful dark-themed HTML report  
- 💬 Clear CLI output with colorized results  
- 🧱 Auto-loads `data.json` platform list  
- 💻 Works on **Linux**, **macOS**, and **Windows**

---

## 🧰 Installation

```bash
git clone https://github.com/GrayVort3x/vosint.git
cd vosint
pip install -r requirements.txt
```

If you plan to use **Tor mode**:
```bash
brew install tor   # macOS
sudo apt install tor -y  # Linux
```

---

## ⚙️ Usage

### Basic
```bash
python3 vosint.py -u username
```

### With speed
```bash
python3 vosint.py -u username -t3
```

### Export as HTML
```bash
python3 vosint.py -u username -oN results.html
```

### Using Proxy
```bash
python3 vosint.py -u username -p http://127.0.0.1:8080
```


---

## 🧩 Example Output

```
__     __        _       _   
\ \   / /__  ___(_)\_ __ | |_ 
 \ \ / / _ \/ __| | '_ \| __|
  \ V / (_) \__ \ | | | | |_ 
   \_/ \___/|___/_|_| |_|\__|

[i] Starting OSINT scan for ali. (Speed: 10)
[+] Found on GitHub: https://github.com/ali
[+] Found on Reddit: https://reddit.com/user/ali
[-] Not found on TikTok
...
[+] Results saved to 'results.html'
```

---

## 🛡️ Ethical Use Disclaimer

Vosint is developed **for educational and ethical purposes only**.  
The author is **not responsible for misuse or illegal activity** conducted with this tool.  
Always respect privacy and local laws when performing OSINT research.

---

## 👨‍💻 Developer

**Author:** Coderianx
**Team:** VortexTeam  
**Year:** 2025  
**License:** MIT

---

## ⭐ Support

If you like Vosint, please give it a ⭐ on GitHub — it motivates continued development!
