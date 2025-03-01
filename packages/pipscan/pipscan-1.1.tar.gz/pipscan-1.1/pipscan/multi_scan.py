import concurrent.futures
import socket

def scan_port(ip, port, timeout):
    """Scans a single port and returns the port if it's open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)  # Increase timeout for slower networks, but adjust as needed

    try:
        if s.connect_ex((ip, port)) == 0:
            return port  # Return the open port
    except:
        pass
    finally:
        s.close()
    
    return None  # Return None if the port is not open

def multi_scan(ip, start_port, end_port, max_threads=100, timeout=1):
    """Scans ports using ThreadPoolExecutor and lists open ports."""
    print(f"\nScanning {ip} from port {start_port} to port {end_port}\n")
    open_ports = []

    # Using ThreadPoolExecutor to manage threads
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # Map the scan_port function to the range of ports
        results = executor.map(lambda port: scan_port(ip, port, timeout), range(start_port, end_port + 1))

        # Collect open ports
        open_ports = [port for port in results if port is not None]

    # Display results
    if open_ports:
        print(f"Open ports on {ip}: {open_ports}\n")
    else:
        print(f"No open ports found on {ip} between {start_port} and {end_port}.\n")

