import socket

# Set to the same port as in your phone script
laptop_port = 5055

# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', laptop_port))
print(f"Listening for GPS data on port {laptop_port}...")

while True:
    data, addr = s.recvfrom(1024)  # receive data
    gps_data = data.decode()
    print(f"📍 GPS from {addr}: {gps_data}")  # print GPS
