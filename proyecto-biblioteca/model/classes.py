class Bibliotecario:
    def __init__(self, nombre, apellido, correo, contraseña, rut):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__correo = correo
        self.__contraseña = contraseña
        self.__rut = rut

    #Nombre
    def getNombreB(self):
        return self.__nombre
    def setNombreB(self, nombre):
        self.__nombre = nombre

    #Apellido
    def getApellidoB(self):
        return self.__apellido
    def setApellidoB(self, apellido):
        self.__apellido = apellido

    #Correo
    def getCorreoB(self):
        return self.__correo
    def setCorreoB(self, correo):
        self.__correo = correo

    #Contraseña
    def getContraseñaB(self):
        return self.__contraseña
    def setContraseñaB(self, contraseña):
        self.__contraseña = contraseña

    #Rut
    def getRutB(self):
        return self.__rut
    def setRutB(self, rut):
        self.__rut = rut

class Usuario:
    def __init__(self, nombre, apellido, direccion, rut, celular, correo, tipo):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__direccion = direccion
        self.__rut = rut
        self.__celular = celular
        self.__correo = correo
        self.__tipo = tipo

    # Nombre
    def getNombreU(self):
        return self.__nombre
    def setNombreU(self, nombre):
        self.__nombre = nombre

    # Apellido
    def getApellidoU(self):
        return self.__apellido
    def setApellidoU(self, apellido):
        self.__apellido = apellido

    # Dirección
    def getDireccionU(self):
        return self.__direccion
    def setDireccionU(self, direccion):
        self.__direccion = direccion

    # Rut
    def getRutU(self):
        return self.__rut
    def setRutU(self, rut):
        self.__rut = rut

    # Celular
    def getCelularU(self):
        return self.__celular
    def setCelularU(self, celular):
        self.__celular = celular

    # Correo
    def getCorreoU(self):
        return self.__correo
    def setCorreoU(self, correo):
        self.__correo = correo

    # Tipo
    def getTipoU(self):
        return self.__tipo
    def setTipoU(self, tipo):
        self.__tipo = tipo