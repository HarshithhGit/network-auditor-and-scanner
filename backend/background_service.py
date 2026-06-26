import time
import requests
from scanner import scan_target
from vulnerability import analyze_vulnerabilities

API_URL = "http://127.0.0.1:8000"

def start_virtual_iot_device():
    print("Virtual IoT Device Scanner Started...")
    target_ip = "127.0.0.1" # Scanning localhost
    while True:
        try:
            print(f"[IoT Device] Scanning target: {target_ip}...")
            open_ports = scan_target(target_ip)
            vulnerabilities = analyze_vulnerabilities(open_ports)
            
            payload = {
                "target_ip": target_ip,
                "open_ports": open_ports,
                "vulnerabilities": vulnerabilities
            }
            
            print(f"[IoT Device] Found {len(open_ports)} open ports and {len(vulnerabilities)} vulnerabilities. Sending to backend...")
            resp = requests.post(f"{API_URL}/api/scan/submit", json=payload)
            print(f"[IoT Device] Server response: {resp.status_code}")
            
        except requests.exceptions.ConnectionError:
            print("[IoT Device] Backend not reachable. Retrying in 60s...")
        except Exception as e:
            print(f"[IoT Device] Error: {e}")
            
        time.sleep(60)

if __name__ == "__main__":
    start_virtual_iot_device()
