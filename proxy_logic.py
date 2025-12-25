import socket
import time
from enum import Enum

SERVER_IP = "192.168.30.90"
CLIENT_IP = "192.168.40.50"
PROXY_IP_CLIENTSIDE = "192.168.40.80"
PROXY_IP_SERVERSIDE = "192.168.30.80"
TFTP_PORT = 69

class OPCode(Enum):
    RRQ = 1
    WRQ = 2
    DATA = 3
    ACK = 4
    ERROR = 5

class Proxy:
    def __init__(self, animation_queue) -> None:
        self.animation_queue = animation_queue
        print("The proxy is ready")

    def __get_sender_from_ip(self, ip) -> str:
        if "40.50" in ip or ip == "127.0.0.1": 
            return "Client"
        elif "30.90" in ip:
            return "Server"
        return "Client"

    def get_opcode(self, packet) -> int:
        return packet[1]

    def get_blocknumber(self, packet) -> int:
        return int.from_bytes(packet[2:4], "big")

    def __get_filename(self, packet) -> str:
        return packet[2:packet.find(b"\00", 2)].decode("ascii")

    def receive(self, socket):
        packet, address = socket.recvfrom(1024)
        sender = self.__get_sender_from_ip(address[0])
        
        # Determine Color and Label for Clarity
        pkt_color = (100, 255, 100) # Default Green
        pkt_label = "TFTP"
        
        if len(packet) >= 2:
            opcode = packet[1]
            if opcode == 3: 
                pkt_color = (0, 100, 255) # Blue for DATA
                pkt_label = f"DATA:{self.get_blocknumber(packet)}"
            elif opcode == 4: 
                pkt_color = (255, 255, 0) # Yellow for ACK
                pkt_label = f"ACK:{self.get_blocknumber(packet)}"

        time.sleep(0.2)

        self.animation_queue.put({
            'f': sender, 't': 'Proxy', 
            'l': pkt_label, 'c': pkt_color 
        })
        return (packet, address)

    def forward(self, socket, address, packet, label_override=None, color_override=None):
        # Determine logical destination
        dest_name = "Server" if address[0] == SERVER_IP else "Client"

        # Apply Scenario Overrides or Automatic Colors
        pkt_label = label_override if label_override else "FORWARD"
        pkt_color = color_override if color_override else (100, 255, 100)
        
        if not label_override and len(packet) >= 2:
            opcode = packet[1]
            if opcode == 3: 
                pkt_label, pkt_color = f"DATA:{self.get_blocknumber(packet)}", (0, 100, 255)
            elif opcode == 4: 
                pkt_label, pkt_color = f"ACK:{self.get_blocknumber(packet)}", (255, 255, 0)

        time.sleep(0.2)

        self.animation_queue.put({
            'f': 'Proxy', 't': dest_name, 
            'l': pkt_label, 'c': pkt_color 
        })
        socket.sendto(packet, address)

# ======================================================================================================================
# SCENARIOS (UNCHANGED LOGIC, UPDATED CALLS)
# ======================================================================================================================

def handle_normal_transmission(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    reset = False; connected = False; last_ack = -1; last_block = -1
    server_address = (SERVER_IP, TFTP_PORT)
    while True:
        if reset:
            server_address = (SERVER_IP, TFTP_PORT); reset = False; connected = False; last_ack = -1; last_block = -1
        if connected:
            request, client_address = proxy.receive(proxy_to_client_socket)
        else:
            request, client_address = proxy.receive(initial_proxy_socket); connected = True
        
        if proxy.get_opcode(request) == OPCode.ACK.value:
            if proxy.get_blocknumber(request) == last_ack: reset = True
        elif proxy.get_opcode(request) == OPCode.DATA.value:
            if len(request) - 4 < 512: last_block = proxy.get_blocknumber(request)
        
        proxy.forward(proxy_to_server_socket, server_address, request)
        if not reset:
            response, server_address = proxy.receive(proxy_to_server_socket)
            if proxy.get_opcode(response) == OPCode.DATA.value:
                if len(response) - 4 < 512: last_ack = proxy.get_blocknumber(response)
            elif proxy.get_opcode(response) == OPCode.ACK.value:
                if proxy.get_blocknumber(response) == last_block: reset = True
            elif proxy.get_opcode(response) == OPCode.ERROR.value: reset = True
            proxy.forward(proxy_to_client_socket, client_address, response)

def increase_payload_size_over_512_bytes(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    first_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, first_packet)
    data_packet, server_address = proxy.receive(proxy_to_server_socket)
    modified_data_packet = bytearray(data_packet) + (b"A" * 100)
    proxy.forward(proxy_to_client_socket, client_address, modified_data_packet, label_override="OVERSIZED", color_override=(255, 0, 0))

def change_ack_block_number(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    first_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, first_packet)
    data_packet, server_address = proxy.receive(proxy_to_server_socket)
    proxy.forward(proxy_to_client_socket, client_address, data_packet)
    ack_packet, client_address = proxy.receive(proxy_to_client_socket)
    modified_ack = bytearray(ack_packet); modified_ack[2] = 0xFF; modified_ack[3] = 0xFF
    proxy.forward(proxy_to_server_socket, server_address, modified_ack, label_override="BAD BLOCK#", color_override=(255, 255, 0))

def delay_data_packet(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    rrq_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, rrq_packet)
    data_packet, server_address = proxy.receive(proxy_to_server_socket)
    time.sleep(25)
    proxy.forward(proxy_to_client_socket, client_address, data_packet, label_override="DELAYED", color_override=(255, 165, 0))

def delay_ack_packet_rrq(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    rrq_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, rrq_packet)
    data1, server_address = proxy.receive(proxy_to_server_socket)
    proxy.forward(proxy_to_client_socket, client_address, data1)
    ack1, client_address = proxy.receive(proxy_to_client_socket)
    time.sleep(25)
    proxy.forward(proxy_to_server_socket, server_address, ack1, label_override="DELAYED ACK", color_override=(255, 165, 0))

def replace_data_with_error_wrq(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    wrq_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, wrq_packet)
    ack_init, server_address = proxy.receive(proxy_to_server_socket)
    proxy.forward(proxy_to_client_socket, client_address, ack_init)
    data_packet, client_address = proxy.receive(proxy_to_client_socket)
    error_packet = bytearray(b"\x00\x05\x00\x04") + b"DATA replaced by ERROR\x00"
    proxy.forward(proxy_to_server_socket, server_address, error_packet, label_override="INJECTED ERROR", color_override=(255, 0, 0))

def send_malformed_packet_rrq(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    rrq_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, rrq_packet)
    data_packet, server_address = proxy.receive(proxy_to_server_socket)
    malformed = bytearray(b"\x00\x03\x00\x01") + b"InvalidPayload"
    proxy.forward(proxy_to_client_socket, client_address, malformed, label_override="MALFORMED", color_override=(255, 0, 255))

def ack_instead_of_forwarding_data_rrq(proxy, initial_proxy_socket, proxy_to_server_socket, proxy_to_client_socket):
    server_address = (SERVER_IP, TFTP_PORT)
    rrq_packet, client_address = proxy.receive(initial_proxy_socket)
    proxy.forward(proxy_to_server_socket, server_address, rrq_packet)
    data_packet, server_address = proxy.receive(proxy_to_server_socket)
    ack_packet = bytearray(b"\x00\x04") + data_packet[2:4]
    proxy.forward(proxy_to_server_socket, server_address, ack_packet, label_override="SPOOFED ACK", color_override=(0, 255, 255))