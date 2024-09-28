import socket
from pynput.mouse import Listener, Controller

# Set up the UDP client
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.0.214', 5000)  # Replace with your second screen's IP address

# Mouse controller to set mouse position
mouse = Controller()

# Variable to store the last valid Y position and monitor control state
last_y = 0
on_secondary_screen = False  # Tracks if we are controlling the secondary screen

# Define the screen width (primary screen width) - adjust this value to your actual resolution
primary_screen_width = 1920  # Example: 1920px for primary screen width

# Define the function to handle mouse movement
def on_move(x, y):
    global last_y, on_secondary_screen
    
    # Case 1: Mouse goes off the left side (x < 0) to switch to secondary screen
    if x < 0 and not on_secondary_screen:
        print(f"Mouse offscreen left! Switching to secondary screen...")
        on_secondary_screen = True
        last_y = y  # Track the Y position for returning later

        # Send a message to start controlling the secondary screen
        message = f"SWITCH_SCREEN,{x},{y}".encode()
        udp_socket.sendto(message, server_address)

    # Case 2: Mouse goes off the right side (x > primary_screen_width) to return to primary screen
    elif x > primary_screen_width and on_secondary_screen:
        print(f"Returning to primary screen from secondary screen...")
        on_secondary_screen = False
        last_y = y  # Track the Y position for returning

        # Send a message to return control to the primary screen
        message = f"RETURN_SCREEN,{x},{y}".encode()
        udp_socket.sendto(message, server_address)

    # Case 3: Normal movements on the primary screen
    elif 0 <= x <= primary_screen_width and not on_secondary_screen:
        last_y = y
        message = f"{x},{y}".encode()
        udp_socket.sendto(message, server_address)

    # Optional: If you want to handle specific movements on the secondary screen while it's controlling the mouse,
    # you could implement additional logic here when `on_secondary_screen` is True.

# Start listening to the mouse movement
def start_udp_client():
    print("Starting UDP client and listening for mouse movement...")
    with Listener(on_move=on_move) as listener:
        listener.join()  # This keeps the listener running to capture events

start_udp_client()
