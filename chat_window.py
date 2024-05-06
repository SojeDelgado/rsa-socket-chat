import socket
import threading

import tkinter as tk
from tkinter import scrolledtext

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12000

class Chat_Window(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.title("Chat RSA")
        self.minsize(480, 640)
        self.config(padx=35, pady=35)

        label_title = tk.Label(self, text="Mensajería segura usando RSA", font=("Arial", 14))
        label_title.grid(column=1, row=1)

        label_llave = tk.Label(self, text="Claves públicas:", font=("Arial", 14))
        label_llave.grid(column=0, row=2)

        self.text_public_keys = scrolledtext.ScrolledText(self,width=20, height=20, state="disabled")
        self.text_public_keys.grid(column=0, row=3, padx=30)

        self.chat_area = scrolledtext.ScrolledText(self, width=50, height=20)
        self.chat_area.grid(column=1, row=3, padx=15)
        self.chat_area.config(state="disabled")

        self.entry_message = tk.Entry(self, width=20, font=("Arial", 14))
        self.entry_message.grid(column=1, row=4, pady=10)

        self.button_send = tk.Button(self, text="Send", font=("Arial", 14), command=self.send_message)
        self.button_send.grid(column=1, row=5)

        self.parent = parent
        self.username = username

        self.socket_instance = socket.socket()

        # Iniciar hilo para manejar la comunicación con el servidor
        threading.Thread(target=self.connect_to_server).start()

    def connect_to_server(self):
        try:
            self.socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
            self.socket_instance.send(self.username.encode())
            print('Connected to chat!')
            self.receive_messages()
        except Exception as e:
            print(f'Error connecting to server socket: {e}')

    def receive_messages(self):
        while True:
            try:
                message = self.socket_instance.recv(1024).decode()
                self.display_message(message)
            except Exception as e:
                print(f'Error receiving message: {e}')
                break

    def send_message(self):
        message = self.entry_message.get()
        if message:
            try:
                self.socket_instance.send(message.encode())
                self.display_message(f"You: {message}")
                self.entry_message.delete(0, tk.END)
            except Exception as e:
                print(f'Error sending message: {e}')
        else:
            print("Please enter a message.")

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.see(tk.END)  # Scroll to the bottom
        self.chat_area.config(state="disabled")

    def close_previous_window(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    username = input("Enter your username: ")
    chat_window = Chat_Window(root, username)
    root.mainloop()
