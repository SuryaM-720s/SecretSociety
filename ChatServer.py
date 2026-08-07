import socket
import json
import threading
import argparse
import time
import sys
import signal

clients = {}
channels = {}
last_activity = time.time()
max_threads = 100
active_threads = 0


# Function to broadcast a message to all clients in the same channel
def handle_client(client_socket, client_address):
    global clients, channels, last_activity, active_threads
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = {'address': client_address, 'nickname': nickname, 'channel': None}
        broadcast_message(client_socket, f"{nickname} has joined the chat.")

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    last_activity = time.time()
                    try:
                        message_data = json.loads(message)
                        process_command(client_socket, message_data)
                    except json.JSONDecodeError:
                        broadcast_message(client_socket, f"{clients[client_socket]['nickname']}: {message}")
                else:
                    remove_client(client_socket)
                    break
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                remove_client(client_socket)
                break

        disconnect_client(client_socket)
    finally:
        active_threads -= 1


# Function to process commands from clients
def process_command(client_socket, message):
    cmd_type = message.get('type')

    if cmd_type == "nick":
        nickname = message.get('nickname')
        clients[client_socket]['nickname'] = nickname
        send_to_client(client_socket, f"Nickname set to {nickname}")

    elif cmd_type == "join":
        channel = message.get('channel')
        join_channel(client_socket, channel)

    elif cmd_type == "list":
        list_channels = {ch: len(users) for ch, users in channels.items()}
        send_to_client(client_socket, {"type": "channel_list", "channels": list_channels})

    elif cmd_type == "leave":
        leave_channel(client_socket)

    elif cmd_type == "quit":
        disconnect_client(client_socket)

    elif cmd_type == "message":
        text = message.get('message')
        broadcast_message(client_socket, f"{clients[client_socket]['nickname']}: {text}")


# Join a channel
def join_channel(client_socket, channel):
    previous_channel = clients[client_socket]['channel']
    if previous_channel and previous_channel in channels:
        channels[previous_channel].remove(client_socket)

    channels.setdefault(channel, []).append(client_socket)
    clients[client_socket]['channel'] = channel
    send_to_client(client_socket, f"Joined channel {channel}")


# Leave a channel
def leave_channel(client_socket):
    channel = clients[client_socket]['channel']
    if channel and channel in channels:
        channels[channel].remove(client_socket)
        clients[client_socket]['channel'] = None
        send_to_client(client_socket, f"Left channel {channel}")


# Function to broadcast a message to all clients in the same channel
def broadcast_message(sender_socket, message):
    sender_info = clients.get(sender_socket)
    if not sender_info:
        return

    channel = sender_info['channel']

    if not channel or channel not in channels:
        send_to_client(sender_socket, "You are not in any channel.")
        return

    for client_socket in channels[channel]:
        if client_socket != sender_socket:
            send_to_client(client_socket, message)


# Function to send a message to a specific client
def send_to_client(client_socket, data):
    try:
        if isinstance(data, str):
            data = {"type": "message", "message": data}
        message = json.dumps(data)
        client_socket.sendall(message.encode('utf-8'))
    except Exception:
        remove_client(client_socket)


# Function to disconnect a client
def disconnect_client(client_socket):
    remove_client(client_socket)
    client_socket.close()


# Function to remove a client from the server
def remove_client(client_socket):
    if client_socket in clients:
        nickname = clients[client_socket]['nickname']
        channel = clients[client_socket]['channel']
        if channel and channel in channels:
            if client_socket in channels[channel]:
                channels[channel].remove(client_socket)
        del clients[client_socket]
        broadcast_message(client_socket, f"{nickname} has left the chat.")


# Function to shutdown server if idle for too long
def shutdown_if_idle():
    global last_activity
    while True:
        time.sleep(10)
        if time.time() - last_activity > 180:  # 3 minutes
            print("No activity detected. Shutting down server.")
            for client_socket in list(clients.keys()):
                disconnect_client(client_socket)
            sys.exit(0)


# Graceful shutdown with Ctrl+C
def graceful_shutdown(sig, frame):
    print("\nServer shutting down gracefully...")
    for client_socket in list(clients.keys()):
        disconnect_client(client_socket)
    sys.exit(0)

#main function to start the server
def main():
    global active_threads

    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('-p', type=int, default=5555, help='Port number')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, graceful_shutdown)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', args.p))
    server_socket.listen(5)
    print(f"Server listening on port {args.p}")

    threading.Thread(target=shutdown_if_idle, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        if active_threads >= max_threads:
            send_to_client(client_socket, "Server busy. Try again later.")
            client_socket.close()
            continue

        active_threads += 1
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


if __name__ == "__main__":
    main()
