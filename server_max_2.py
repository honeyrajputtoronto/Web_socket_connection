import socket
import threading
import json

IP = socket.gethostbyname(socket.gethostname())
PORT = 5567
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
questions = {
    "Q1": {
        "question": "Which among the following is not a computer language?",
        "answers": ["ALGOL", "COBOL", "PASCAL", "DRAM"],
        "correct_ans": "DRAM",
    },
    "Q2": {
        "question": "1 Gigabyte (Gb) =",
        "answers": ["1024 Mb", "1000 Mb", "1200 Mb", "1275 Mb"],
        "correct_ans": "1024 Mb",
    },
    "Q3": {
        "question": "In JS if you add [1, 2, 3] + [4, 5, 6] will result to?",
        "answers": ["[1, 2, 3, 4, 5, 6]", "[1, 2, 34, 5, 6]", "[[1, 2, 3], [4, 5, 6]]", "ERROR"],
        "correct_ans": "[1, 2, 34, 5, 6]",
    },
    "Q4": {
        "question": "A web address is usually known as …",
        "answers": ["URL", "UWL", "WWW", "UVL"],
        "correct_ans": "URL",
    },
    "Q5": {
        "question": "Who was the father of computer?",
        "answers": ["Charlie Babbage", "Dennis Ritchie", "Charles Babbage", "Ken Thompson"],
        "correct_ans": "Charles Babbage",
    },
    "Q6": {
        "question": "Mi hamelek shel CSS?",
        "answers": ["NETANEL", "NETANEL", "NETANEL", "NETANEL"],
        "correct_ans": "NETANEL",
    }

}

# Counter for connected clients
client_count = 0

def handle_client(conn, addr):
    global client_count
    print(f"[NEW CONNECTION] {addr} connected.")
    
    level = 1
    print(f'Welcome to Battle')

    # Increment client count and check if it exceeds the limit
    client_count += 1
    if client_count > 2:
        # print(f"[SERVER FULL] {addr} was rejected due to maximum occupancy.")
        # conn.send("Server is full. Try again later.".encode(FORMAT))
        conn.close()
        client_count -= 1  # Decrement client count if rejected
        return

    connected = True
    while connected:
        question_str = json.dumps(questions)  # Convert questions to a JSON string

        conn.send(question_str.encode(FORMAT))

        answer = conn.recv(SIZE).decode(FORMAT)
        if answer == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] Answer: {answer}")

    # Decrement client count when client disconnects
    client_count -= 1
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        # Check if maximum client count reached
        if client_count >= 2:
            print("[SERVER FULL] Maximum client count reached. Closing server...")
            break

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

    # Close the server socket
    server.close()

if __name__ == "__main__":
    main()
