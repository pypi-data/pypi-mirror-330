# PyDefender

## 🛡️ Anti-VM & Sandbox Detection for Python

PyDefender is a Python package designed to detect virtual machines, sandboxes, and automated analysis environments. It helps protect your scripts from running in controlled environments often used for malware analysis or security research.

## 📜 Features
- Detects popular virtual machines (VMware, VirtualBox, Hyper-V, etc.).
- Identifies sandbox environments used for malware analysis.
- Checks system artifacts to determine if running in a VM.
- Supports Windows and Linux.
- Lightweight and easy to integrate.

## 🚀 Installation
Install PyDefender via pip:

```sh
pip install pydefender
```

## 🔍 Usage
Here's how to use PyDefender in your Python project:

```python
import pydefender

def main():
    if pydefender.is_vm():
        print("Virtual machine detected! Exiting...")
        exit()
    else:
        print("Running on a physical machine.")

if __name__ == "__main__":
    main()
```

## 🖥️ Detection Methods
PyDefender uses multiple techniques to detect virtualized environments:
- **System Manufacturer Check**: Identifies VM vendors from system metadata.
- **MAC Address Check**: Detects VM-related network adapter addresses.
- **Registry & File Artifacts** (Windows): Looks for VM-specific registry keys and files.
- **CPU & Memory Anomalies**: Checks for signs of virtualized CPU and memory configurations.
- **Process & Service Analysis**: Scans for known VM or sandbox processes.

## ⚠️ Disclaimer
PyDefender is intended for ethical and legitimate purposes only. Do not use it for malicious activities. The developers are not responsible for misuse of this software.