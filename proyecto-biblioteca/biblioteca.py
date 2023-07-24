from customtkinter import *
from client.gui_app import Frame

# Version 0.00001

def main():
    root = CTk()
    root.title('Biblioteca Virtual')
    root.iconbitmap('img\libros.ico')
    root.resizable(0,0)
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    height = 650
    width = 1240
    x = (root.winfo_screenwidth()//2) - (width//2)
    y = (root.winfo_screenheight()//4) - (height//4)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    ventana_principal = Frame(root = root)
    ventana_principal.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

if __name__ == "__main__":
    main()