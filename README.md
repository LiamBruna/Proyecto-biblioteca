# Proyecto-biblioteca

1. Clonar Repo: `git clone https://github.com/Ven0s00/Proyecto-biblioteca.git`  
2. Abrir Carpeta y Terminal en VSCode Respectivamente  
3. Crear Entorno: `py -m venv env`  
4. Instalar Módulos: `pip install -r requirements.txt`
5. Abrir variable de entorno virtual: `env\Scripts\activate.bat`


6. Cambios en la Base de Datos: Se elimino la columna CATALOGO de la tabla libro
7. Nuevo modulo a instalar:  `tkcalendar`
8. Numero de celular para la aplicación: `+14178554277`
9. credenciales dentro: TWILIO_ACCOUNT_SID=ACc5fcca03bf8e78a8d943d1e71c0099ed, 
TWILIO_AUTH_TOKEN=8e549a03d607cdd90de517a898026b20
10. Cambios en la Base de Datos: Tabla bibliotecario se añadio CELULAR_B
11. Cambios en la Base de Datos: Tabla prestamo se añadio RUT_U, ISBN, TIPO_U, ID_B
12. Cambios en la Base de Datos: Tabla ejemplares => ejemplar y se añadio ID_L como FK referencia a ID_L de la tabla libro
13. Nuevo modulo a instalar `twilio`
14. Nuevo modulo a instalar: `watchdog`


Sprint 1:
semana entera 3 horas al día = 21 horas
Frame Ventana de logeo ✔️
Frame actualizar stock ✔️
Frame usuarios registrados ✔️
Frame realizar préstamo ✔️
Frame libros en préstamo ✔️
Frame renovar libro ✔️
Frame ventana de registro ✔️

Sprint 2
Semana entera 3 horas al dia = 21 horas
Funciones actualizar stock ✔️
Funciones usuarios registrados ✔️
Funciones realizar préstamo ✔️
Funciones libros en préstamo ✔️
Funciones registrar usuarios✔️
Funciones renovar libro ✔️
Funciones cerrar sesión, cambiar apariencia de app, registrarse y cambiar contraseña✔️

Sprint 3
Semana entera 3 horas al dia = 21 horas
Se agrego barra de progreso
Frame catalogo


Modificaciones en la base de datos

- Tabla usuario se añadió TIPO_u
- Tabla préstamo se añadió RUT_U, ISBN, TIPO_U, ID_B, RENOVADO
- Tabla bibliotecario se añadió CELULAR_B
- Tabla ejemplares se cambio el nombre a "ejemplar" y se añadió ISBN
- Tabla libro se elimino columna CATALOGO