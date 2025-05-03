# ezenvpro

**Simplify IP & Host Management | Streamline Your Pentesting Workflow and OSCP Methodology 🚨**

---

##  Overview

ezenvpro is your go-to CLI tool designed specifically for pentesters, OSCP aspirants, and network enthusiasts. Effortlessly manage IP addresses, environment variables, and `/etc/hosts` entries—no more typos, tedious notes, or cross-referencing IPs and URLs. Spend less time setting up, more time hacking!

---

## ⚡ Key Benefits

* **Fast & Efficient**: Instantly set IPs and hostnames.
* **Zero Hassle**: Automate environment variable and `/etc/hosts` management.
* **Mistake-Proof**: Avoid IP/URL typos with handy aliases.
* **OSCP-Ready**: Ideal for fuzzing, scanning, and smooth exam workflows.
* **User-Friendly**: Intuitive prompts with clear, colorful terminal output.

---

## 💻 Installation

### Quick Install (Recommended)

```bash
pipx install ezenvpro
```

### Manual Setup

Clone and install manually:

```bash
git clone [<repo-url>](https://github.com/d0mi33/ezenvpro.git)
cd ezenvpro
chmod +x ezenvpro.py
sudo cp ezenvpro.py /usr/local/bin/ezenvpro
```

### Dependencies

```bash
pip3 install colorama
```

---

## 🛠️ How to Use

```bash
ezenvpro [-h] [-n N] [-t TAGS] [-g GROUP] [-o] [-d VARS] [-a ALIAS] [-s]
```

### Quick Examples

Set IPs with custom tags, groups, and HTTPS aliases:

```bash
ezenvpro -n 2 -t web01 db01 -g clientX -a -s
```

Add URL aliases to existing IP variables:

```bash
ezenvpro -a ca_ip1 ca_ip2 -s
```

Delete environment variables and hosts entries:

```bash
ezenvpro -d ca_ip1
```

---

## 📌 Quick Notes

* **Root Privileges**: Use `sudo` for `/etc/hosts` modifications.
* **Apply Changes Immediately**:

```bash
source ~/.zshrc
```

---

## 🚧 Preview

```
✅  Changes saved!

🔄 Apply immediately:

╔═══════════════════════════════════════╗
║ → RUN: source ~/.zshrc                ║
║ → OR open a new terminal window       ║
╚═══════════════════════════════════════╝
```

---

## 📃 License

MIT License. Open-source & community-driven.

---

**Crafted by Dominic Thirshatha (@d0mi33)**
