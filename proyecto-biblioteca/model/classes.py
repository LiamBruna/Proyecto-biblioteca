class Bibliotecario:
    def __init__(self, nombre, apellido, correo, contraseña, rut):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__correo = correo
        self.__contraseña = contraseña
        self.__rut = rut


    #Nombre
    def getNombre(self):
        return self.__nombre
    def setNombre(self, nombre):
        self.__nombre = nombre

    #Apellido
    def getApellido(self):
        return self.__apellido
    def setApellido(self, apellido):
        self.__apellido = apellido

    #Correo
    def getCorreo(self):
        return self.__correo
    def setCorreo(self, correo):
        self.__correo = correo

    #Contraseña
    def getContraseña(self):
        return self.__contraseña
    def setContraseña(self, contraseña):
        self.__contraseña = contraseña

    #Rut
    def getRut(self):
        return self.__rut
    def setRut(self, rut):
        self.__rut = rut