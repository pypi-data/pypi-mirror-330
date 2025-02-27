#!/usr/bin/env python3
import json
import os
import platform
import socket
import subprocess
import threading
from datetime import datetime

import requests
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML as FormattedHTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from pathlib import Path


class SSHManager:
    def __init__(self):
        self.credentials_file = os.path.expanduser('~/.ssh_manager/credentials.json')
        self.passwords_file = os.path.expanduser('~/.ssh_manager/passwords.json')
        self.logs_dir = f"{Path(__file__).parent}"
        self.history_file = os.path.expanduser('~/.ssh_manager/history')
        self.ensure_credentials_dir()
        self.load_credentials()
        self.load_passwords()

        self.style = Style.from_dict({
            'prompt': '#00FFFF bold',  # Cyan
            'hostname': '#00FF00',  # Green
            'username': '#FFFF00',  # Yellow
            'error': '#FF0000 bold',  # Red
            'success': '#00FF00',  # Green
            'warning': '#FFFF00',  # Yellow
        })

        self.commands = {
            'add': self.add_credential,
            'add-password': self.add_credential_with_password,
            'list': self.list_credentials,
            'connect': self.connect_ssh,
            'remove': self.remove_credential,
            'edit': self.edit_credential,
            'clear': self.clear_screen,
            'cls': self.clear_screen,
            'myip': self.show_ip_addresses,
            'status': self.check_server_status,
            'history': self.show_history,
            'help': self.show_help,
            'exit': self.exit_app
        }

        self.command_completer = WordCompleter(list(self.commands.keys()))
        self.command_history = []

    def load_passwords(self):
        try:
            with open(self.passwords_file, 'r') as f:
                self.passwords = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.passwords = {}

    def save_passwords(self):
        with open(self.passwords_file, 'w') as f:
            json.dump(self.passwords, f, indent=4)

    def load_credentials(self):
        try:
            with open(self.credentials_file, 'r') as f:
                self.credentials = json.load(f)
        except json.JSONDecodeError:
            self.credentials = {}

    def save_credentials(self):
        with open(self.credentials_file, 'w') as f:
            json.dump(self.credentials, f, indent=4)

    def add_credential(self):
        name = input("Enter a name for this connection: ").strip()
        hostname = input("Enter hostname: ").strip()
        username = input("Enter username: ").strip()
        port = input("Enter port (default: 22): ").strip() or "22"

        self.credentials[name] = {
            "hostname": hostname,
            "username": username,
            "port": port
        }
        self.save_credentials()
        print(f"Credentials saved for {name}")

    def add_credential_with_password(self):
        name = input("Enter a name for this connection: ").strip()
        hostname = input("Enter hostname: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password (leave empty for key-based auth): ").strip()
        port = input("Enter port (default: 22): ").strip() or "22"

        self.credentials[name] = {
            "hostname": hostname,
            "username": username,
            "port": port
        }
        self.save_credentials()
        if password:
            self.passwords[name] = password
            self.save_passwords()
            print(f"Credentials and password saved for {name}")
        else:
            print(f"Credentials saved for {name} (no password stored)")

    def list_credentials(self):
        if not self.credentials:
            print("No saved credentials found.")
            return

        print("\nSaved SSH Connections:")
        print("-" * 50)
        for name, details in self.credentials.items():
            print(f"Name: {name}")
            print(f"Host: {details['hostname']}")
            print(f"User: {details['username']}")
            print(f"Port: {details['port']}")
            # print(f"Password: {'Stored' if name in self.passwords else 'Not stored'}")
            print("-" * 50)

    def remove_credential(self):
        if not self.credentials:
            print("No saved credentials found.")
            return

        print("\nAvailable connections:")
        for name in self.credentials.keys():
            print(f"- {name}")

        name = input("\nEnter connection name to remove: ").strip()
        if name in self.credentials:
            del self.credentials[name]
            self.save_credentials()
            if name in self.passwords:
                del self.passwords[name]
                self.save_passwords()

            print(f"Removed credentials for {name}")
        else:
            print("Connection not found!")

    def edit_credential(self):
        if not self.credentials:
            print("No saved credentials found.")
            return

        print("\nAvailable connections:")
        for name in self.credentials.keys():
            print(f"- {name}")

        name = input("\nEnter connection name to edit: ").strip()
        if name not in self.credentials:
            print("Connection not found!")
            return

        current = self.credentials[name]
        print(f"\nEditing connection: {name}")
        print("(Press Enter to keep current value)")

        new_hostname = input(f"Enter hostname [{current['hostname']}]: ").strip()
        new_username = input(f"Enter username [{current['username']}]: ").strip()
        new_port = input(f"Enter port [{current['port']}]: ").strip()

        has_password = name in self.passwords
        password_prompt = "Update password? (y/n): " if has_password else "Add password? (y/n): "
        if input(password_prompt).lower().strip() == 'y':
            new_password = input("Enter new password: ").strip()
            if new_password:
                self.passwords[name] = new_password
            elif has_password:
                del self.passwords[name]
        self.credentials[name] = {
            "hostname": new_hostname if new_hostname else current['hostname'],
            "username": new_username if new_username else current['username'],
            "port": new_port if new_port else current['port']
        }

        new_name = input(f"Enter new name for connection (or Enter to keep '{name}'): ").strip()
        if new_name and new_name != name:
            self.credentials[new_name] = self.credentials.pop(name)
            if name in self.passwords:
                self.passwords[new_name] = self.passwords.pop(name)
            print(f"Connection renamed to {new_name}")

        self.save_credentials()
        self.save_passwords()
        print("Connection updated successfully!")

    def exit_app(self):
        print("quick-ssh exiting...")
        exit(0)

    def clear_screen(self):
        if platform.system().lower() == "windows":
            os.system('cls')
        else:
            os.system('clear')

    def ensure_credentials_dir(self):
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

        if not os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'w') as f:
                json.dump({}, f)

    def connect_ssh(self, server_name=None):
        if not self.credentials:
            print("No saved credentials found. Please add some first.")
            return
        if not server_name:
            print("\nAvailable connections:")
            for name in self.credentials.keys():
                print(f"- {name}")
            server_name = input("\nEnter connection name: ").strip()

        if server_name not in self.credentials:
            print(f"Connection '{server_name}' not found!")
            return

        # log_session = input("Do you want to log this session? (y/n): ").lower().strip() == 'y'
        # log_file = False
        log_session = False
        if log_session:
            default_filename = f"ssh_{server_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_filename = input(f"Enter log filename (default: {default_filename}): ").strip()
            if not log_filename:
                log_filename = default_filename

            if not log_filename.endswith('.log'):
                log_filename += '.log'

            log_file = os.path.join(self.logs_dir, log_filename)
            print(f"Session will be logged to: {log_file}")
        details = self.credentials[server_name]

        if server_name in self.passwords:
            if self.is_sshpass_available():
                cmd = [
                    "sshpass",
                    "-p",
                    self.passwords[server_name],
                    "ssh",
                    f"{details['username']}@{details['hostname']}",
                    "-p",
                    details['port'],
                    "-o",
                    "StrictHostKeyChecking=no"
                ]
            else:
                print("Warning: Password is stored but sshpass is not installed.")
                print("Please install sshpass to use password authentication.")
                print("Falling back to regular SSH connection...")
                cmd = [
                    "ssh",
                    f"{details['username']}@{details['hostname']}",
                    "-p",
                    details['port']
                ]
        else:
            cmd = [
                "ssh",
                f"{details['username']}@{details['hostname']}",
                "-p",
                details['port']
            ]

        print(f"\nConnecting to {details['hostname']}...")

        if log_session:
            self.connect_and_log(cmd, log_file, server_name, details)
        else:
            subprocess.run(cmd)

    def is_sshpass_available(self):
        try:
            subprocess.run(["sshpass", "-V"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def connect_and_log(self, cmd, log_file, name, details):
        with open(log_file, 'w', encoding='utf-8') as log:
            # Write session header
            header = f"\nSSH Session Started at {datetime.now()}\n"
            header += f"Connection: {name}\n"
            header += f"Host: {details['hostname']}\n"
            header += f"User: {details['username']}\n"
            header += f"Port: {details['port']}\n"
            header += f"Command: {' '.join(cmd)}\n"
            header += "=" * 50 + "\n\n"
            log.write(header)
            log.flush()

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            def log_output(pipe, log_file):
                with open(log_file, 'a', encoding='utf-8') as log:
                    for line in pipe:
                        log.write(line)
                        log.flush()
                        print(line, end='')
            stdout_thread = threading.Thread(
                target=log_output,
                args=(process.stdout, log_file)
            )
            stderr_thread = threading.Thread(
                target=log_output,
                args=(process.stderr, log_file)
            )

            stdout_thread.start()
            stderr_thread.start()

            process.wait()

            stdout_thread.join()
            stderr_thread.join()

            with open(log_file, 'a', encoding='utf-8') as log:
                footer = f"\n\nSSH Session Ended at {datetime.now()}\n"
                footer += "=" * 50 + "\n"
                log.write(footer)

    def get_local_ips(self):
        local_ips = []
        try:
            hostname = socket.gethostname()
            addresses = socket.getaddrinfo(hostname, None)
            for addr in addresses:
                ip = addr[4][0]
                # Filter out IPv6 addresses and loopback
                if ':' not in ip and ip != '127.0.0.1':
                    local_ips.append(ip)
            local_ips = list(dict.fromkeys(local_ips))
        except Exception as e:
            local_ips.append(f"Error getting local IP: {str(e)}")
        return local_ips

    def get_public_ip(self):
        ip_services = [
            "https://api.ipify.org",
            "https://api.ip.sb/ip",
            "https://ifconfig.me/ip"
        ]
        for service in ip_services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
        return "Could not determine public IP"

    def show_ip_addresses(self):
        print("\nIP Addresses:")
        print("-" * 50)
        print("Local IP Addresses:")
        local_ips = self.get_local_ips()
        for ip in local_ips:
            print(f"  • {ip}")
        print("\nPublic IP Address:")
        print(f"  • {self.get_public_ip()}")
        print("-" * 50)

    def print_styled(self, text, style_name):
        print_formatted_text(
            FormattedHTML(f'<{style_name}>{text}</{style_name}>'),
            style=self.style
        )

    def ping_host(self, host):
        try:
            if platform.system().lower() == "windows":
                command = ["ping", "-n", "1", "-w", "2000", host]
            else:
                command = ["ping", "-c", "1", "-W", "2", host]
            result = subprocess.run(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            return result.returncode == 0
        except:
            return False

    def check_ssh_port(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False

    def get_styled_text(self, text, style_name):
        return HTML(f'<{style_name}>{text}</{style_name}>')

    def show_detailed_status(self, host, port):
        try:
            ip = socket.gethostbyname(host)
            ping_ok = self.ping_host(host)
            ssh_ok = self.check_ssh_port(host, port)

            print(f"\nDetailed Status for {host}")
            print("-" * 50)
            print(f"IP Address: {ip}")
            print(f"Ping Status: {'Success' if ping_ok else 'Failed'}")
            print(f"SSH Status: {'Available' if ssh_ok else 'Unavailable'}")

            if ssh_ok:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((host, port))
                    banner = sock.recv(1024).decode().strip()
                    sock.close()
                    print(f"SSH Banner: {banner}")
                except:
                    print("SSH Banner: Unable to retrieve")
            print("-" * 50)

        except socket.gaierror:
            print(f"Unable to resolve hostname: {host}")
        except Exception as e:
            print(f"Error checking status: {str(e)}")

    def check_server_status(self, server_name=None):
        if not self.credentials:
            self.print_styled("No saved credentials found.", "warning")
            return
        if not server_name:
            print("\nAvailable connections:")
            for name in self.credentials.keys():
                print(f"- {name}")
            server_name = input("\nEnter server name to check (press Enter to check all): ").strip()
        print("\nChecking server status...")
        print("-" * 50)

        if server_name:
            if server_name in self.credentials:
                details = self.credentials[server_name]
                self._check_single_server(server_name, details)
            else:
                self.print_styled(f"Server '{server_name}' not found!", "error")
        else:
            for name, details in self.credentials.items():
                self._check_single_server(name, details)

    def _check_single_server(self, name, details):
        host = details['hostname']
        port = int(details['port'])
        start_time = datetime.now()
        is_ping_ok = self.ping_host(host)
        ping_time = (datetime.now() - start_time).total_seconds() * 1000  # Convert to ms
        is_ssh_ok = self.check_ssh_port(host, port)

        ping_status = "✓" if is_ping_ok else "✗"
        ssh_status = "✓" if is_ssh_ok else "✗"

        status = "ONLINE" if is_ping_ok and is_ssh_ok else "OFFLINE"

        # Print with proper formatting
        self.print_styled(f"Server: {name}", "hostname")
        print(f"Host: {host}")
        # self.print_styled(f"Ping: {ping_status}", 'success' if is_ping_ok else 'error')
        self.print_styled(f"Ping: {ping_status} ({ping_time:.1f}ms)", 'success' if is_ping_ok else 'error')
        self.print_styled(f"SSH (Port {port}): {ssh_status}", 'success' if is_ssh_ok else 'error')
        self.print_styled(f"Status: {status}", 'success' if status == "ONLINE" else 'error')
        print("-" * 50)

    def add_to_history(self, command):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"{timestamp} - {command}"

        # self.command_history.append(history_entry)
        # print(f'history: {history_entry}')
        # # Save to history file
        # with open(self.history_file, 'a') as f:
        #     f.write(history_entry + '\n')

    def show_history(self):
        try:
            with open(self.history_file, 'r') as f:
                history = f.readlines()

            if not history:
                print("No command history found.")
                return

            print("\nCommand History:")
            print("-" * 50)

            for entry in history[-20:]:
                print(entry.strip())

            print("-" * 50)
            print(f"Showing last 20 commands. Total commands: {len(history)}")
        except FileNotFoundError:
            print("No command history found.")

    def show_help(self):
        self.print_styled("\nAvailable commands:", "prompt")
        commands_help = [
            ("add", "Add new SSH credentials (without password)"),
            # ("add-password", "Add new SSH credentials with password"), not working correctly debugging needed
            ("list", "List saved SSH credentials"),
            ("status  [name]", "Check server status. Optionally specify name to check single server"),
            ("connect [name]", "Connect to a saved SSH session. Optionally specify name directly"),
            ("remove", "Remove saved SSH credentials and password"),
            ("edit", "Edit existing SSH credentials and password"),
            ("clear", "Clear terminal screen (or cls)"),
            ("myip", "Show local and public IP addresses"),
            ("history", "Show command history"),
            ("help", "Show this help message"),
            ("exit", "Exit the application")
        ]

        for cmd, desc in commands_help:
            self.print_styled(f"  {cmd:<14} - {desc}", "hostname")

    def get_styled_text(self, text, style_name):
        return HTML(f'<{style_name}>{text}</{style_name}>')

    def run(self):
        session = PromptSession(
            completer=self.command_completer,
            style=self.style,
            history=FileHistory(self.history_file)
        )
        self.clear_screen()
        self.print_styled("Welcome to Quick-SSH Manager!", "success")
        self.print_styled("Type 'help' for available commands.", "prompt")

        while True:
            try:
                command = session.prompt(
                    FormattedHTML('<prompt>quick-ssh</prompt> > ')
                ).strip()

                if command:
                    parts = command.split()
                    base_command = parts[0].lower()
                    args = parts[1:] if len(parts) > 1 else []

                    self.add_to_history(command)

                    if base_command in self.commands:
                        if base_command == 'connect' and args:
                            self.connect_ssh(args[0])
                        elif base_command == 'status' and args:
                            self.check_server_status(args[0])
                        else:
                            self.commands[base_command]()
                    else:
                        self.print_styled(
                            "Unknown command. Type 'help' for available commands.",
                            "error"
                        )
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
