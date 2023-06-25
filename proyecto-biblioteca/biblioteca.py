import tkinter as tk
from customtkinter import *
from client.gui_app import Frame

def main():
    root = CTkToplevel()
    root.title('Biblioteca')
    root.iconbitmap('img\libros.ico')
    root.resizable(0,0)

    app = Frame(root = root)
    app.mainloop()

if __name__ == "__main__":
    main()