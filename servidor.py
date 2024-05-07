import random
import socket
import threading
import generacion_llaves
from User import User

# Global variable to maintain client connections along with their usernames
connections = {}
users = []

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
    Get user connection in order to keep receiving their messages and
    send them to other users/connections.
    '''
    try:
        # Receive username from the client
        username = connection.recv(1024).decode()
        connections[connection] = username
        print(f'{username} has joined the chat.')

        p = random.randint(10, 100)
        q = random.randint(10, 100)
        n = p * q
        e = generacion_llaves.generate_e(p, q)
        phi_n = generacion_llaves.phi(p, q)
        d = generacion_llaves.mod_inverse(e, phi_n)

        # Llave publica (e,d)
        # Llave privada (d,n)

        # Crear una instancia de User
        user = User(username, [e, d], [d, n])
        users.append(user)
        

        while True:
            imprimir_usuarios(connection)
            msg = connection.recv(1024)
            if msg:
                print(f'{connections[connection]}: {msg.decode()}')
                msg_to_send = f'{connections[connection]}: {msg.decode()}'
                broadcast(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

    except Exception as e:
        print(f'Error handling user connection: {e}')
        remove_connection(connection)


def broadcast(message: str, sender: socket.socket) -> None:
    '''
    Broadcast message to all users connected to the server
    '''
    for client_conn in connections:
        if client_conn != sender:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print(f'Error broadcasting message: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    '''
    Remove specified connection from connections list
    '''
    if conn in connections:
        username = connections[conn]
        print(f'{username} has left the chat.')
        conn.close()
        del connections[conn]
        # Notify all clients about the user leaving
        notify_clients(f'{username} has left the chat.')


def notify_clients(message: str, exclude_client: socket.socket = None) -> None:
    '''
    Send a message to all clients except the specified client (if provided)
    '''
    for client_conn in connections:
        if client_conn != exclude_client:
            try:
                client_conn.send(f'{message}'.encode())
            except Exception as e:
                print(f'Error notifying client: {e}')
                remove_connection(client_conn)


def send_user_list(client_conn: socket.socket) -> None:
    '''
    Send the list of connected users to a client
    '''
    user_list = ', '.join(connections.values())
    try:
        client_conn.send(f'[SERVER_MSG] Connected users: {user_list}'.encode())
    except Exception as e:
        print(f'Error sending user list to client: {e}')
        remove_connection(client_conn)


def imprimir_usuarios(connection: socket.socket) -> None:
    mensaje = "-"
    for u in users:
        mensaje += f"{u.username}, {u.public_key}\n"

    try:
        notify_clients(mensaje, connection)
    except Exception as e:
        print(f'Error sending user list to client: {e}')
        remove_connection(connection)


def server() -> None:
    '''
    Main process that receives client connections and starts a new thread
    to handle their messages
    '''
    LISTENING_PORT = 12000

    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')

        while True:
            socket_connection, address = socket_instance.accept()
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


if __name__ == "__main__":
    server()
