from customtkinter import *
from client.gui_app import Frame

def main():
    root = CTk()
    root.title('Biblioteca')
    root.iconbitmap('img\libros.ico')
    root.resizable(0,0)

    Frame(root = root)
    root.mainloop()

if __name__ == "__main__":
    main()