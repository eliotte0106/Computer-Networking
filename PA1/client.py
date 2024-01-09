import socket
import argparse
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
            sys.stdout.flush()
        except:
            break

def join_server(host, port, username, passcode):
    if len(passcode) > 5:
        print("Incorrect passcode")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(passcode.encode())
    response = client_socket.recv(1024).decode()
    if response == "Connected":
        print(f"Connected to {host} on port {port}")
        client_socket.send(username.encode())
        threading.Thread(target=receive_messages, args=(client_socket,)).start()
        while True:
            message = input()
            # if message == ":Exit":
            #     client_socket.send(message.encode())
            #     break
            # elif message == ":mytime" or message == ":+1hr":
            #     client_socket.send(message.encode())
            #     break
            # message = message.replace(":)", "[feeling happy]").replace(":(", "[feeling sad]")
            client_socket.send(message.encode())
    else:
        print("Incorrect passcode length or value")
        sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client program for multiple client chatroom")
    parser.add_argument("-join", action="store_true", help="Join the server")
    parser.add_argument("-host", type=str, required=True, help="Server hostname")
    parser.add_argument("-port", type=int, required=True, help="Server port")
    parser.add_argument("-username", type=str, required=True, help="Username")
    parser.add_argument("-passcode", type=str, required=True, help="Passcode for the chatroom (max 5 letters)")
    args = parser.parse_args()

    join_server(args.host, args.port, args.username, args.passcode)