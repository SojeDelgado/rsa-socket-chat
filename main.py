import tkinter as tk
from tkinter import messagebox
from chat_window import Chat_Window


def open_new_window():
    nickname = entry_nickname.get()
    if nickname.strip():
        window.withdraw()
        new_window = Chat_Window(window, nickname)
        new_window.protocol("WM_DELETE_WINDOW", lambda: close_new_window(new_window))
    else:
        messagebox.showerror("Error", "Por favor ingrese un nombre de usuario")

def close_new_window(new_window):
    window.deiconify()
    new_window.destroy()

window = tk.Tk()
window.title("RSA Chat")
window.minsize(width=300, height=400)
window.config(padx=35, pady=35)

label_title = tk.Label(text="RSA", font=("Impact", 30), fg="red")
label_title.grid(column=0, row=1)

label_text1 = tk.Label(text="Sistema de", font=("Impact", 20))
label_text1.grid(column=0, row=2)
label_text2 = tk.Label(text="Mensajeria Segura", font=("Impact", 20))
label_text2.grid(column=0, row=3)
label_text3 = tk.Label(text="con RSA", font=("Impact", 20))
label_text3.grid(column=0, row=4)

label_nickname = tk.Label(text="Usuario: ", font=("Arial", 14))
label_nickname.grid(column=0, row=5, pady=15)

entry_nickname = tk.Entry(width=20, font=("Arial", 14))
entry_nickname.grid(column=0, row=6)

button_accept = tk.Button(text="Entrar", font=("Arial", 14), command=open_new_window)
button_accept.grid(column=0, row=7, pady=15)

window.mainloop()


