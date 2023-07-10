from customtkinter import *
from client.gui_app import Frame

# Version 0.00001

def main():
    root = CTk()
    root.title('Biblioteca Virtual')
    root.iconbitmap('img\libros.ico')
    root.resizable(0,0)
    root.geometry("600x440")

    ventana_principal = Frame(root = root)
    ventana_principal.pack()
    root.mainloop()

if __name__ == "__main__":
    main()