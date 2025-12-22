# Cisco-Copycat: TFTP Visual Analyzer 🛡️📊

**Cisco Copycat** is a Python-based network analysis tool designed to intercept, modify, and visualize TFTP (Trivial File Transfer Protocol) traffic in a virtualized environment. By acting as a transparent proxy, the tool allows researchers and students to simulate various network scenarios—from normal file transfers to packet loss and spoofing attacks—while watching the data flow in real-time through a custom Pygame-based GUI.

## 🚀 Key Features

* **Real-time Visualizer**: A high-speed Pygame interface that tracks packets as they move between **Client**, **Proxy**, and **Server**.
* **Color-Coded Traffic**: Instantly distinguish between packet types:
    * 🟦 **Blue**: DATA packets.
    * 🟨 **Yellow**: ACK (Acknowledgment) packets.
    * 🟩 **Green**: Control/RRQ/WRQ packets.
    * 🟥 **Red**: ERROR or Malformed packets.
* **7 Interactive Scenarios**: Test network resilience with built-in scenarios including:
    * **Scenario 3/4**: Simulated 25-second latency.
    * **Scenario 5**: Error injection (replacing DATA with ERROR).
    * **Scenario 7**: ACK Spoofing (intercepting data without forwarding).
* **Packet Inspection**: Dynamic labels showing OpCodes and Block Numbers as packets travel.

## 🛠️ Technology Stack

* **Language**: Python 3.x
* **Visualization**: Pygame
* **Networking**: Raw Sockets & Scapy
* **Environment**: Optimized for Debian Linux VMs (VirtualBox)

## 📥 Installation & Setup

### 1. Prerequisites
Ensure you have Pygame and Scapy installed on your Client VM:
```bash
pip install pygame scapy
