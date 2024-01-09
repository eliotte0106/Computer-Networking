import socket
import argparse
import threading
import sys
import datetime

clients = {}

emoji_map = {
    ":)": "[feeling happy]",
    ":(": "[feeling sad]"
}

def start_server(port, passcode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, passcode)).start()

def broadcast(message, exclude_client=None):
    for username, client_socket in clients.items():
        if client_socket != exclude_client:
            try:
                client_socket.send(message.encode())
            except:
                remove_client(username, client_socket)

def translate_emoji(message):
    for emoji, full_text in emoji_map.items():
        message = message.replace(emoji, f"{full_text}")
    return message

def handle_client(client_socket, passcode):
    client_data = client_socket.recv(1024).decode()

    if len(client_data) <= 5 and client_data == passcode:
        client_socket.send(b"Connected")
        username = client_socket.recv(1024).decode()
        if username not in clients:
            clients[username] = client_socket
            print(f"{username} joined the chatroom")
            sys.stdout.flush()
            join_message = f"{username} joined the chatroom"
            broadcast(join_message, client_socket)
            while True:
                message = client_socket.recv(1024).decode()
                if message == ":Exit":
                    break
                elif message == ":mytime":
                    curr_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
                    #client_socket.send(curr_time.encode())
                    print(f"{curr_time}")
                    sys.stdout.flush()
                    broadcast(f"{curr_time}")
                elif message == ":+1hr":
                    plus_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                    plus_time_str = plus_time.strftime("%a %b %d %H:%M:%S %Y")
                    #client_socket.send(plus_time_str.encode())
                    print(f"{plus_time_str}")
                    sys.stdout.flush()
                    broadcast(f"{plus_time_str}")
                else:
                    message = translate_emoji(message)
                    print(f"{username}: {message}")
                    sys.stdout.flush()
                    broadcast(f"{username}: {message}", client_socket)
            remove_client(username, client_socket)
        else:
            client_socket.send(b"Username already in use in the system")
            client_socket.close()
    else:
        client_socket.send(b"Incorrect passcode")
        client_socket.close()

def remove_client(username, client_socket):
    if username in clients:
        print(f"{username} left the chatroom")
        sys.stdout.flush()
        leave_message = f"{username} left the chatroom"
        broadcast(leave_message)
        del clients[username]
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server program for multiple client chatroom")
    parser.add_argument("-start", action="store_true", help="Start the server")
    parser.add_argument("-port", type=int, required=True, help="Port to listen on")
    parser.add_argument("-passcode", type=str, required=True, help="Passcode for the chatroom (max 5 letters)")
    args = parser.parse_args()

    if args.start:
        start_server(args.port, args.passcode)
    else:
        print("Restart the server")
