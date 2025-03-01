# PipScan

PipScan is a simple and efficient port scanner written in Python. It allows users to scan IP addresses and ports to check for open connections. It is ideal for network administrators and security professionals who need to scan for open ports in their network.

## Features

- Scan a single IP address.
- Multi-threaded scanning to speed up the process.
- Can scan a range of ports.

## Installation

You can install PipScan using pip from the Python Package Index (PyPI):

```bash
pip install pipscan
```

## Usage

- Single Port Scan:
```python
    import pipscan

    pipscan.single_scan('ip', port)
```
- Multi Port Scan
```python
    import pipscan

    pipscan.multi_scan('ip', start_port, end_port, max_threads = threads, timeout = socket_timeout)
```

