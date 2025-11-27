# Cisco CopyCat

## 🚀 Overview
This project is a custom **Client/Server Network Packet Analyzer** built for the Trivial File Transfer Protocol (TFTP). Functioning as a transparent proxy, it sits between a client and server to capture, inspect, and visualize network traffic in real-time.

Designed to meet the requirements of a **Network Packet Analyzer & Display Tool**, it features a **Web-Based Dashboard** to display packet headers (Opcodes, Block Numbers) and an **Active Fault Injection Engine** to simulate network anomalies.

## ⚡ Key Features
* **Packet Analyzer:** Real-time parsing of TFTP protocol headers (RRQ, WRQ, DATA, ACK).
* **Display Tool:** A **Flask-based Web Interface** that visualizes the packet flow in a live table, acting as a visual inspection tool similar to Cisco Packet Tracer's simulation window.
* **Fault Injection:** A suite of test scenarios to simulate "bad situations" for protocol auditing:
    * **Latency:** Simulating network lag on DATA/ACK packets.
    * **Traffic Manipulation:** Modifying Block Numbers and Payload sizes.
    * **Error Injection:** Replacing valid data with protocol error codes.
* **Modular Architecture:** Cleanly separated codebase with distinct modules for the Proxy Core, Web Interface, Configuration, and Fault Scenarios.

## 🛠️ Project Structure
* `main.py` - Entry point that launches the Proxy and Web Server threads.
* `proxy_core.py` - Core logic for packet capturing and parsing.
* `web_interface.py` - Flask application for the visual dashboard.
* `scenarios.py` - Logic for all fault injection simulations.
* `config.py` - Global configuration and shared logging memory.

## 📸 Usage
1. Start the tool: `python3 main.py`
2. Open the Dashboard: `http://localhost:5000`
3. Initiate a TFTP transfer from your client machine.
4. Watch the packets appear live on the web dashboard!
