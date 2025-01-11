import json
import sys
from typing import List, Dict
import subprocess

def load_servers() -> List[Dict]:
    try:
        with open('servers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: servers.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in servers.json")
        sys.exit(1)

def display_servers(servers: List[Dict]) -> None:
    print("\nAvailable servers:")
    for i, server in enumerate(servers, 1):
        print(f"{i}. {server['name']} ({server['ip']})")

def connect_to_server(server: Dict) -> None:
    ssh_command = f"sshpass -p {server['password']} ssh {server['username']}@{server['ip']} -p {server.get('port', 22)}"
    print(f"\nConnecting to {server['name']}...")
    try:
        subprocess.run(ssh_command, shell=True)
    except KeyboardInterrupt:
        print("\nConnection terminated by user")

def main():
    servers = load_servers()
    while True:
        display_servers(servers)
        try:
            choice = input("\nSelect a server number (or 'q' to quit): ")
            if choice.lower() == 'q':
                break
            
            server_index = int(choice) - 1
            if 0 <= server_index < len(servers):
                connect_to_server(servers[server_index])
            else:
                print("Invalid server number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")

if __name__ == "__main__":
    main() 