import socket
import threading
import json

from colorama import Fore

Server = None
Port = None
client_socket = None
nickname = None
connected = False
color = None


# Thread to receive messages from server
def receive_messages():
    global connected
    while connected:
        try:
            #Receive data from server
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("Disconnected from server.")
                connected = False
                break

            try:
                #Recover JSON messages
                msg = json.loads(data)
                msg_type = msg.get("type", "")
                # Handle different message types
                if msg_type == "message":
                    print(msg.get("message"))
                elif msg_type == "channel_list": 
                    print("Channels:")
                    for ch, users in msg["channels"].items():
                        print(f"  {ch}: {users} user(s)")
                else:
                    print(data)
            except json.JSONDecodeError:
                print(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            connected = False
            break

# Function to connect to server
def connect_to_server(server_ip, server_port):
    global client_socket, connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        connected = True
        print("Connected to the server.")
# Start thread to receive messages
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        print(f"Connection error: {e}")
        connected = False

# Helper to send JSON messages to server
def send_json(data):
    """Helper to send JSON messages to server."""
    global client_socket
    try:
        msg = json.dumps(data)
        client_socket.sendall(msg.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

# Function to color text based on user choice
def color_text(text, color):
    color_map = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "BLUE": Fore.BLUE,
        "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE
    }
    return color_map.get(color.upper(), Fore.WHITE) + text + Fore.RESET

# Main function
def main():
    global nickname, connected, color

# Get server details and nickname from user
    color =  input("Choose your text color (RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE): ").upper()
    server_ip = input(getattr(Fore, color, "") + "Enter server IP address: ")
    server_port = int(input("Enter server port: "))
    nickname = input("Enter your nickname: ")

    connect_to_server(server_ip, server_port)

    if connected:
        # Send nickname first as plain text (required by server)
        client_socket.send(nickname.encode('utf-8'))
        print("Type /help for commands.")

        while connected:
            msg = input()
# Handle commands
            #/nick command
            if msg.startswith("/nick"):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    send_json({"type": "nick", "nickname": parts[1]})
                else:
                    print("Usage: /nick <nickname>")
            #/join command
            elif msg.startswith("/join"):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    send_json({"type": "join", "channel": parts[1]})
                else:
                    print("Usage: /join <channel>")
            #/list command
            elif msg.startswith("/list"):
                send_json({"type": "list"})
            #/leave command
            elif msg.startswith("/leave"):
                send_json({"type": "leave"})
            #/quit command
            elif msg.startswith("/quit"):
                send_json({"type": "quit"})
                connected = False
                break
            #/help command
            elif msg.startswith("/help"):
                print("""
Available commands:
/connect <server-name> [port#]
/nick <nickname>
/list
/join <channel>
/leave [<channel>]
/quit
/help
/color <color>
                """)
            #/color command
            elif msg.startswith("/color"):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    color = parts[1].upper()
                    print(color_text("Text color changed.", color))
                    print(getattr(Fore, color, ""))
                else:
                    print("Usage: /color <color>")
            else:
                # Normal chat message
                send_json({"type": "message", "message": msg})

    else:
        print(Fore.WHITE)

# Cleanup on exit
        client_socket.close()
        print(Fore.WHITE)
        print("Disconnected from server.")


if __name__ == "__main__":
    main()

