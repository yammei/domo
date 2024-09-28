import socket
import pyautogui

def start_udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 5123))

    print("Server is listening for incoming UDP messages...")

    while True:
        data, addr = udp_socket.recvfrom(16)
        x, y = map(int, data.decode().split(","))
        pyautogui.moveTo(x, y, duration=0.1)

start_udp_server()
