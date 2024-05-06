import socket
import threading

def handle_messages(connection: socket.socket):
    '''
    Receive messages sent by the server and display them to the user
    '''
    while True:
        try:
            msg = connection.recv(1024)

            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def client() -> None:
    '''
    Main process that starts client connection to the server
    and handles its input messages
    '''

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))

        # Prompt the user for their username
        username = input("Enter your username: ")

        # Send the username to the server
        socket_instance.send(username.encode())

        # Create a thread to handle messages sent by the server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to chat!')

        # Read user's input until they quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(msg.encode())

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
