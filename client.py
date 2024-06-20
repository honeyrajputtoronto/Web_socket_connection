import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5239
ADDR = (IP, PORT)
SIZE = 6094
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        question = client.recv(SIZE).decode(FORMAT)
        print(f"Question: {question}")

        answer = input("> ")
        client.send(answer.encode(FORMAT))

        if answer == DISCONNECT_MSG:
            connected = False

    client.close()

if __name__ == "__main__":
    main()
