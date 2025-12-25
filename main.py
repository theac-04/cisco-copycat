import threading
import queue
import socket
import sys
from visualizer import TFTPVisualizer
import proxy_logic as pl

def read_user_input() -> int:
    """Reads user input to select the network scenario"""
    print("\n" + "="*50)
    print("TFTP DISPLAY ANALYZER - SELECT SCENARIO")
    print("="*50)
    print("0: Normal transmission")
    print("1: Increase payload size over 512 bytes (WRQ/RRQ)")
    print("2: Change Block Number of ACK packet (RRQ/WRQ)")
    print("3: Delay DATA packet for 25 seconds (RRQ)")
    print("4: Delay ACK packet for 25 seconds (RRQ)")
    print("5: Replace DATA packet with ERROR packet (WRQ)")
    print("6: Send malformed packet (RRQ)")
    print("7: Spoof ACK to server (Do not forward DATA)")
    print("="*50)
    
    try:
        return int(input("Enter choice [0-7]: "))
    except ValueError:
        return 0

def main():
    animation_queue = queue.Queue()
    viz = TFTPVisualizer(animation_queue)

    def proxy_task():
        proxy = pl.Proxy(animation_queue)
        try:
            initial_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            initial_sock.bind((pl.PROXY_IP_CLIENTSIDE, pl.TFTP_PORT))

            server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Use eth0 for the Internal Network connection
            server_sock.setsockopt(socket.SOL_SOCKET, 25, str("eth0" + "\0").encode("ascii"))

            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            choice = read_user_input()
            print(f"\n[SYSTEM] Starting Scenario {choice}...")

            if choice == 0:
                pl.handle_normal_transmission(proxy, initial_sock, server_sock, client_sock)
            elif choice == 1:
                pl.increase_payload_size_over_512_bytes(proxy, initial_sock, server_sock, client_sock)
            elif choice == 2:
                pl.change_ack_block_number(proxy, initial_sock, server_sock, client_sock)
            elif choice == 3:
                pl.delay_data_packet(proxy, initial_sock, server_sock, client_sock)
            elif choice == 4:
                pl.delay_ack_packet_rrq(proxy, initial_sock, server_sock, client_sock)
            elif choice == 5:
                pl.replace_data_with_error_wrq(proxy, initial_sock, server_sock, client_sock)
            elif choice == 6:
                pl.send_malformed_packet_rrq(proxy, initial_sock, server_sock, client_sock)
            elif choice == 7:
                pl.ack_instead_of_forwarding_data_rrq(proxy, initial_sock, server_sock, client_sock)

        except Exception as e:
            print(f"[ERROR] Proxy failed: {e}")

    t = threading.Thread(target=proxy_task, daemon=True)
    t.start()
    print("[SYSTEM] Launching Visualizer Window...")
    viz.run()

if __name__ == "__main__":
    main()