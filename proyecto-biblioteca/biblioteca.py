import tkinter as tk
import customtkinter as ck
from client.gui_app import Frame

def main():
    root = tk.Tk()
    root.title('Biblioteca')
    root.iconbitmap('img/libros.ico')
    root.resizable(False, False)

    app = Frame(root=root)
    app.mainloop()

if __name__ == "__main__":
    main()