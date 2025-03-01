import socket

def single_scan(ip, port):
    """Scans a single port, detects service, and grabs banners if possible."""
    print(f"\nScanning {ip} with port {port}\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  

    try:
        s.connect((ip, port))
        service = socket.getservbyport(port, "tcp") if port <= 49151 else "Unknown"
        print(f"[+] Port {port} is OPEN ({service})\n")

        # Banner grabbing
        try:
            s.send(b"Hello\r\n")
            banner = s.recv(1024).decode().strip()
            if banner:
                print(f"    └─ Banner: {banner}")
        except:
            pass

    except:
        print(f"Port {port} is not open on IP {ip}.\n")

    finally:
        s.close()
