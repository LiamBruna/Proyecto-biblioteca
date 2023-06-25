import tkinter as tk
import customtkinter as ck
from client.gui_app import Frame

def main():
    root = ck.CTk()
    root.title('Biblioteca')
    root.iconbitmap('img\libros.ico')
    root.resizable(0,0)

    app = Frame(root = root)
    app.mainloop()

if __name__ == "__main__":
    main()