import time
import socket
from backend.scanner import scan_target
from backend.vulnerability import analyze_vulnerabilities
from backend.password_auditor import audit_password

def display_menu():
    print("\n" + "="*70)
    print(" IoT Vulnerability Scanner & Password Auditor (Terminal)")
    print("="*70)
    print(" 1. Scan Surrounding IP Address (Find Weak Networks & Faults)")
    print(" 2. Test Password Strength")
    print(" 3. Exit Demo")
    print("="*70)

def get_risk_symbol(risk):
    risk = risk.lower()
    if risk in ['none', 'low']:
        return "🟩 [✓] NO RISK / LOW RISK"
    elif risk == 'medium':
        return "🟨 [!] MEDIUM RISK"
    else:
        return "🟥 [X] HIGH RISK / CRITICAL"

def get_crack_method(port):
    methods = {
        21: "Attackers use tools like Hydra to brute-force FTP logins and access files.",
        22: "Attackers map default usernames (root) and use dictionary lists to crack SSH.",
        23: "Telnet is entirely unencrypted. Attackers use Wireshark to sniff the network and steal passwords.",
        80: "Plaintext HTTP exposes sessions. Attackers perform a Man-in-the-Middle (MitM) attack to hijack cookies.",
        445: "Ransomware worms (like WannaCry) use exploits like EternalBlue to silently take over the workstation.",
        3389: "Automated brute-force bots continuously attack RDP to install crypto-lockers and steal data.",
        3306: "Exposed databases are targeted by credential stuffing to dump all user tables.",
        5432: "Similar to MySQL, attackers brute-force default 'postgres' user accounts.",
        27017: "Automated scripts scan for unauthenticated MongoDB instances, wipe the data, and demand a ransom."
    }
    return methods.get(port, "Attackers scan this service for known version vulnerabilities to run remote code.")

def run_scan_demo():
    print("\n[*] Initializing Network Scanner...")
    print("Hint: You can enter '127.0.0.1' for localhost, or another IP like '192.168.1.5'")
    target = input("Enter an IP address to scan: ").strip()
    
    if not target:
        target = "127.0.0.1"
        
    print(f"\n[*] Scanning target IP: {target}...")
    time.sleep(1) # Fake delay for effect
    
    print("[*] Checking for open ports and tracking weak networks...")
    open_ports = scan_target(target)
    
    if not open_ports:
        print("[-] No common open ports found on this system.")
        print(get_risk_symbol('Low'))
    else:
        print(f"\n[+] Found {len(open_ports)} active open ports on the network:")
        for p in open_ports:
            print(f"    -> Port {p['port']} [{p.get('service', 'Unknown')}]")
            
        print("\n[*] Passing data to Vulnerability Engine to find weak networks...")
        time.sleep(1.5)
        
        vulns = analyze_vulnerabilities(open_ports)
        if not vulns:
            print(get_risk_symbol("Low") + " System appears secure based on known port security rules.")
        else:
            print(f"\n[!] WARNING: Found {len(vulns)} system vulnerabilities!\n")
            for v in vulns:
                symbol = get_risk_symbol(v['risk'])
                print(f"{symbol} -> Port {v['port']} ({v['service']})")
                print(f"     Risk Issue:     {v['issue']}")
                print(f"     How to Crack:   {get_crack_method(v['port'])}")
                print(f"     Details:        {v['detail']}\n")
    
    input("Press Enter to return to menu...")

def run_password_demo():
    print("\n[*] Initializing Password Auditor...")
    pwd = input("Enter a password to test (Will not be saved): ")
    
    print("[*] Analyzing entropy, dictionary lists, and complexity...")
    time.sleep(0.7)
    
    result = audit_password(pwd)
    
    print("\n--- Password Audit Results ---")
    print(f" Password length: {len(pwd)}")
    print(f" Score:           {result['score']} / 100")
    print(f" Risk Symbol:     {get_risk_symbol(result['risk'])}")
    print(f" Entropy:         {result['entropy']} bits")
    print(f" Est. Crack Time: {result['crack_time']}")
    print(f" Feedback:        {result['feedback']}")
    print("------------------------------")
    
    input("Press Enter to return to menu...")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            run_scan_demo()
        elif choice == '2':
            run_password_demo()
        elif choice == '3':
            print("Exiting Demo Tool. Stay secure!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
