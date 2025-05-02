#!/usr/bin/env python3
import os
import argparse
import ipaddress
import sys
import readline
from colorama import Fore, Style, init
import re

def is_valid_varname(name):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

# Initialize colorama for colored text
init()

ZSHRC = os.path.expanduser("~/.zshrc")
HOSTS = "/etc/hosts"

def display_banner():
    print(Fore.CYAN + r"""
███████╗███████╗███████╗██╗███████╗███████╗███████╗██╗   ██╗
██╔════╝╚══███╔╝╚══███╔╝██║╚══███╔╝╚══███╔╝╚══███╔╝╚██╗ ██╔╝
█████╗    ███╔╝   ███╔╝ ██║  ███╔╝   ███╔╝   ███╔╝  ╚████╔╝ 
██╔══╝   ███╔╝   ███╔╝  ██║ ███╔╝   ███╔╝   ███╔╝    ╚██╔╝  
███████╗███████╗███████╗██║███████╗███████╗███████╗   ██║   
╚══════╝╚══════╝╚══════╝╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   
""")
    print(Fore.RED + "           ezenvpro v 1.0zzzz")
    print(Fore.CYAN + "        Infra Pentest Environment Manager")
    print(Fore.RED + "\n       Created by Dominic Thirshatha @d0mi33\n" + Style.RESET_ALL)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def safe_input(prompt):
    try:
        return input(Fore.GREEN + " >> " + Fore.YELLOW + prompt + Style.RESET_ALL).strip()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Operation cancelled by user." + Style.RESET_ALL)
        sys.exit(1)

def write_to_zshrc(line, override=False):
    if not os.path.exists(ZSHRC):
        open(ZSHRC, "w").close()
    with open(ZSHRC, "r") as f:
        lines = f.readlines()
    key = line.split("=")[0].replace("export ", "").strip()
    if override:
        lines = [l for l in lines if not l.startswith(f"export {key}=")]
    elif any(l.startswith(f"export {key}=") for l in lines):
        print(Fore.YELLOW + f"[!] {key} already exists. Use --override to replace." + Style.RESET_ALL)
        return
    lines.append(f"{line}\n")
    with open(ZSHRC, "w") as f:
        f.writelines(lines)
    print(Fore.GREEN + f"[+] Added {key} to ~/.zshrc" + Style.RESET_ALL)

def update_hosts(ip, hostname):
    if os.geteuid() != 0:
        print(Fore.RED + "[!] You must run this script as root to update /etc/hosts." + Style.RESET_ALL)
        print(Fore.YELLOW + "[!] If /etc/hosts changes fail, try running sudo ezenvpro." + Style.RESET_ALL)
        return
    entry = f"{ip} {hostname}"
    with open(HOSTS, "r") as f:
        if entry in f.read():
            print(Fore.YELLOW + f"[-] /etc/hosts already contains: {entry}" + Style.RESET_ALL)
            return
    with open(HOSTS, "a") as f:
        f.write(f"{entry}\n")
    print(Fore.GREEN + f"[+] Added {entry} to /etc/hosts" + Style.RESET_ALL)

def delete_var(varname):
    ip_value = None
    url_varname = f"url_{varname}"

    if not os.path.exists(ZSHRC):
        print(Fore.RED + "[!] .zshrc does not exist." + Style.RESET_ALL)
        return

    with open(ZSHRC, "r") as f:
        lines = f.readlines()
        for l in lines:
            if l.startswith(f"export {varname}="):
                ip_value = l.split("=", 1)[1].strip()
                break

    new_lines = [l for l in lines if not l.startswith(f"export {varname}=") and not l.startswith(f"export {url_varname}=")]
    with open(ZSHRC, "w") as f:
        f.writelines(new_lines)

    print(Fore.GREEN + f"[+] Removed {varname} and {url_varname} from ~/.zshrc" + Style.RESET_ALL)

    if ip_value:
        try:
            with open(HOSTS, "r") as f:
                hosts_lines = f.readlines()
            new_hosts_lines = [line for line in hosts_lines if not line.startswith(ip_value)]
            if len(new_hosts_lines) != len(hosts_lines):
                with open(HOSTS, "w") as f:
                    f.writelines(new_hosts_lines)
                print(Fore.GREEN + f"[+] Removed related /etc/hosts entry for IP {ip_value}" + Style.RESET_ALL)
        except PermissionError:
            print(Fore.RED + "[!] Permission denied: run as root to modify /etc/hosts" + Style.RESET_ALL)

def add_url_aliases(varnames, protocol="http", override=False):
    for var in varnames:
        value = None
        if os.path.exists(ZSHRC):
            with open(ZSHRC, "r") as f:
                for line in f:
                    if line.startswith(f"export {var}="):
                        value = line.split("=", 1)[1].strip()
                        break
        if value and is_valid_ip(value):
            url_var = f"url_{var}"
            write_to_zshrc(f"export {url_var}={protocol}://{value}", override=override)
        else:
            print(Fore.RED + f"[!] Could not find valid IP for variable '{var}' in ~/.zshrc" + Style.RESET_ALL)

def print_reload_message():
    print(Fore.BLUE + "🔄 To apply the change now, either:")
    print(Fore.GREEN + Style.BRIGHT + r"""
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║   → RUN: source ~/.zshrc              ║
    ║                                       ║
    ║   → OR open a new terminal tab/window ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def main():
    display_banner()

    parser = argparse.ArgumentParser(
        description="ezenvpro - Infra pentest IP manager",
        epilog="Examples:\n  ezenvpro -n 2 -t web01 db01 -g clientX -a -s\n  ezenvpro -a ca_ip1 ca_ip2 -s\n  ezenvpro -d ca_ip1",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-n", type=int, help="Number of IPs to set")
    parser.add_argument("--tags", "-t", nargs="*", help="Custom tags like dc1 web01 etc.")
    parser.add_argument("--group", "-g", help="Group name prefix")
    parser.add_argument("--override", "-o", action="store_true", help="Override existing entries")
    parser.add_argument("--delete", "-d", nargs="+", help="Delete one or more variables and their aliases")
    parser.add_argument("--alias", "-a", nargs="+", help="Add alias for existing or new var(s)")
    parser.add_argument("--secure", "-s", action="store_true", help="Use https:// instead of http://")

    args = parser.parse_args()

    if args.delete:
        for var in args.delete:
            delete_var(var)
        print(Fore.CYAN + "\n✅  Deletion complete.")
        print_reload_message()
        return

    if args.alias and not args.n:
        protocol = "https" if args.secure else "http"
        add_url_aliases(args.alias, protocol=protocol, override=args.override)
        print(Fore.CYAN + "\n✅  Aliases added to existing variables.")
        print_reload_message()
        return

    if not args.n and (args.tags or args.group):
        parser.print_help()
        print(Fore.RED + "\n[!] Missing -n flag. You must specify number of IPs to input.\n" + Style.RESET_ALL)
        return


    if args.n:
        tags = args.tags if args.tags else [f"ip{i+1}" for i in range(args.n)]
        if len(tags) != args.n:
            print(Fore.RED + "[!] Number of tags must match number of IPs." + Style.RESET_ALL)
            return

    # Validate tag names
        for tag in tags:
            if not is_valid_varname(tag):
                print(Fore.RED + f"[!] Invalid tag name '{tag}': must start with a letter or underscore and contain only letters, digits, or underscores." + Style.RESET_ALL)
                sys.exit(1)
        group_prefix = f"{args.group}_" if args.group else ""
    

        for i in range(args.n):
            tag = tags[i]
            varname = f"{group_prefix}{tag}"
            while True:
                ip = safe_input(f"Enter IP for {varname}: ")
                if is_valid_ip(ip):
                    break
                print(Fore.RED + "[!] Invalid IP address. Please try again." + Style.RESET_ALL)
            hostname = safe_input(f"Enter hostname for {varname}: ")
            write_to_zshrc(f"export {varname}={ip}", override=args.override)
            update_hosts(ip, hostname)

            if args.alias:
                protocol = "https" if args.secure else "http"
                url_var = f"url_{varname}"
                write_to_zshrc(f"export {url_var}={protocol}://{ip}", override=args.override)

        print(Fore.CYAN + "\n✅  Requested Changes have been written")
        print_reload_message()

def cli():
    main()

if __name__ == "__main__":
    main()

