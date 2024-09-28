import socket

def start_udp_server():
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to an IP address and port
    udp_socket.bind(('0.0.0.0', 5000))  # Listening on all network interfaces on port 5000

    print("UDP server is listening on port 5000...")

    # Continuously listen for messages
    while True:
        data, addr = udp_socket.recvfrom(1024)  # Receive up to 1024 bytes
        print(f"Received message: {data.decode()} from {addr}")

# Start the server
start_udp_server()
