import socket

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
HEADER_LENGTH = 10
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def send_message(client_socket, message):
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER_LENGTH - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message.encode(FORMAT))


def receive_message(client_socket):
    message_length = client_socket.recv(HEADER_LENGTH).decode(FORMAT)
    if message_length:
        message_length = int(message_length)
        return client_socket.recv(message_length).decode(FORMAT)
    return None


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[CONNECTED TO SERVER] Welcome!")

    while True:
        topic = input("What do you want a fact about (Cats, Dogs, Sloths, YouTube or quit):")
        if topic.lower() == "quit":
            print("Goodbye!")
            send_message(client_socket, DISCONNECT_MESSAGE)
            break
        send_message(client_socket, topic)
        response = receive_message(client_socket)
        print(response)

    client_socket.close()


if __name__ == "__main__":
    main()
