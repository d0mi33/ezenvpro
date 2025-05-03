# ezenvpro
**Simplify IP & Host Management | Streamline Your Pentesting Workflow and OSCP Methodology 🚨**

![SS](/img/ez5.png)

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
![gif1](/img/demo.gif)

### Manual Setup

Clone and install manually:

```bash
git clone https://github.com/d0mi33/ezenvpro.git
cd ezenvpro
chmod +x ezenvpro.py
sudo cp ezenvpro.py /usr/local/bin/ezenvpro
ezenvpro -h
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

Set IPs with custom tags, groups, and HTTPS/HTTP aliases:

```bash
ezenvpro -n 2 -t dc1 db01 -g clientX -a -s
```
![gif2](/img/initial.gif)

Add URL aliases to existing IP variables, so that you can do subdirectory fuzing with just the variables and don't have to type the full URL every time! -a for http:// and -s for https://

```bash
ezenvpro -a dc1 -s
```

Delete environment variables and hosts entries:

```bash
ezenvpro -d dc1
```
![img](/img/delete.jpeg)
---

## Quick Notes

* **Root Privileges**: Use `sudo` for `/etc/hosts` modifications.
* **Apply Changes Immediately**: open a new terminal or run
* **Groups are tags that act as a prefix for every tag to organise variables if working with multiple hosts.**: -g / --group
* **Override lets you replace an existing IP in the ~/.zshrc**: -o / --override
* **tags default starts with ip1,ip2...**: if -t / --tags not specified

```bash
source ~/.zshrc
```

---

## 🚧 Preview
![img2](/img/help.jpeg)

---

## 📃 License

MIT License. Open-source & community-driven.

---

**Crafted by Dominic Thirshatha (@d0mi33)**
