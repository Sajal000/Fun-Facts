import socket
import random

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
HEADER_LENGTH = 10
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

facts = {
    "cats": [
        "Cats sleep for about 70% of their lives.",
        "Cats make about 100 different sounds",
        "Cats are North America’s most popular pet.",
        "Cats can rotate their ears 180 degrees.",
        "A group of cats is called a clowder."
    ],
    "dogs": [
        "The French Bulldog was named the most popular breed in 2022",
        "Dogs' sense of hearing is more than ten times more acute than a human's.",
        "Seventy percent of people sign their dog’s name on their holiday cards",
        "Dogs' nose prints are as unique as human fingerprints.",
        "All dogs dream, but puppies and senior dogs dream more frequently than adult dogs"
    ],
    "sloths": [
        "Sloths are the slowest mammals on Earth.",
        "Sloths can sleep up to 20 hours per day.",
        "Sloths have very low metabolic rates and slow digestion, taking up to a month to digest a single meal.",
        "Without sloths, we might not have avocados! The extinct giant ground sloths were among the few mammals "
        "capable of digesting huge avocado seeds whole. They feasted on avocados and dispersed the seeds far and "
        "wide. All tree sloths we see today evolved from these giants.",
        "Sloths are excellent swimmers! They occasionally drop from their treetop perches into water for a paddle."
    ],
    "youtube": [
        "YouTube was founded on February 14, 2005, by three ex-PayPal employees.",
        "The first-ever YouTube video was uploaded on April 23, 2005, featuring one of its co-founders at the San "
        "Diego Zoo.",
        "Every minute, over 100 hours of video are uploaded to YouTube.",
        "YouTubers collectively watch 6 billion hours of videos per month and 4 billion videos every day.",
        "YouTube is the second-most popular website globally, right after Google Search"
    ]
}


def handle_client(client_socket):
    print("[NEW CONNECTION]")
    connected = True
    while connected:
        topic_length = client_socket.recv(HEADER_LENGTH).decode(FORMAT)
        if topic_length:
            topic_length = int(topic_length)
            topic = client_socket.recv(topic_length).decode(FORMAT)
            if topic == DISCONNECT_MESSAGE:
                connected = False
            else:
                fact = "Hmmmm.... I am not familiar with that"
                if topic.lower() in facts:
                    fact = random.choice(facts[topic.lower()])
                fact_length = len(fact.encode(FORMAT))
                send_length = str(fact_length).encode(FORMAT)
                send_length += b' ' * (HEADER_LENGTH - len(send_length))
                client_socket.send(send_length)
                client_socket.send(fact.encode(FORMAT))
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen()
    print(f"[LISTENING] {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, client_address = server.accept()
        handle_client(client_socket)


start_server()
