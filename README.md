# Cisco Copycat: TFTP Visual Analyzer 🛡️📊

**Cisco Copycat** is a Python-based network analysis tool designed to intercept, modify, and visualize TFTP traffic in a virtualized environment. It acts as a transparent proxy, allowing you to simulate and watch network scenarios in real-time through a Pygame GUI.

## 🚀 Key Features
* **Real-time Visualizer**: Tracks packets moving between **Client**, **Proxy**, and **Server**.
* **Color-Coded Traffic**: 🟦 DATA (Blue), 🟨 ACK (Yellow), 🟩 Control (Green), 🟥 ERROR (Red).
* **7 Scenarios**: Includes normal transmission, packet delays (25s), oversized payloads, and ACK spoofing.

## 📥 Setup
1. **Install Dependencies**: `pip install pygame scapy`
2. **Network**: Use VirtualBox **Internal Network**. Client IP: `192.168.40.80`, Server IP: `192.168.30.90`.
3. **Run**: `sudo python3 main.py`

---
**Authors**: Theodora-Mihaela Cimpoeru & Cristian Radu
