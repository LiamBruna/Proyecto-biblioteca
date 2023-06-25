BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "autor" (
	"ID_A"	INTEGER,
	"NOMBRE_A"	TEXT,
	"APELLIDO_A"	TEXT,
	"NACIONALIDAD"	TEXT,
	PRIMARY KEY("ID_A" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "contiene" (
	"ID_E"	INTEGER NOT NULL,
	"ID_P"	INTEGER NOT NULL,
	PRIMARY KEY("ID_E","ID_P"),
	FOREIGN KEY("ID_E") REFERENCES "ejemplares"("ID_E"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P")
);
CREATE TABLE IF NOT EXISTS "ejemplares" (
	"ID_E"	INTEGER,
	"ID_L"	INTEGER NOT NULL,
	"ESTADO"	TEXT NOT NULL,
	PRIMARY KEY("ID_E" AUTOINCREMENT),
	FOREIGN KEY("ID_L") REFERENCES "libro"("ID_L")
);
CREATE TABLE IF NOT EXISTS "escribe" (
	"ID_A"	INTEGER NOT NULL,
	"ID_L"	INTEGER NOT NULL,
	PRIMARY KEY("ID_A","ID_L"),
	FOREIGN KEY("ID_L") REFERENCES "libro"("ID_L"),
	FOREIGN KEY("ID_A") REFERENCES "autor"("ID_A")
);
CREATE TABLE IF NOT EXISTS "libro" (
	"ID_L"	INTEGER,
	"ISBN"	TEXT NOT NULL,
	"TITULO"	TEXT NOT NULL,
	"NUMERO_PAGINAS"	INTEGER,
	"CATALOGO"	TEXT,
	"STOCK"	INTEGER NOT NULL,
	PRIMARY KEY("ID_L" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "pide" (
	"ID_U"	INTEGER NOT NULL,
	"ID_P"	INTEGER NOT NULL,
	PRIMARY KEY("ID_U","ID_P"),
	FOREIGN KEY("ID_U") REFERENCES "usuario"("ID_U"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P")
);
CREATE TABLE IF NOT EXISTS "registra" (
	"ID_P"	INTEGER NOT NULL,
	"ID_B"	INTEGER NOT NULL,
	PRIMARY KEY("ID_P","ID_B"),
	FOREIGN KEY("ID_B") REFERENCES "bibliotecario"("ID_B"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P")
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"ID_U"	INTEGER,
	"NOMBRE_U"	TEXT,
	"APELLIDO_U"	TEXT,
	"DIRECCION_U"	TEXT,
	"RUT_U"	TEXT NOT NULL,
	"CELULAR_U"	INTEGER,
	"CORREO_U"	TEXT,
	"TIPO_U" TEXT,
	PRIMARY KEY("ID_U" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "bibliotecario" (
	"ID_B"	INTEGER,
	"NOMBRE_B"	TEXT,
	"APELLIDO_B"	TEXT,
	"CORREO_B"	VARCHAR NOT NULL,
	"CONTRASENA"	VARCHAR(100) NOT NULL,
	"RUT_B"	TEXT,
	PRIMARY KEY("ID_B" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "prestamo" (
	"ID_P"	INTEGER,
	"F_PRESTAMO"	TEXT NOT NULL,
	"F_DEVOLUCION"	TEXT NOT NULL,
	"ID_B"	INTEGER,
	PRIMARY KEY("ID_P" AUTOINCREMENT),
	FOREIGN KEY("ID_B") REFERENCES "bibliotecario"("ID_B")
);
INSERT INTO "bibliotecario" VALUES (21,'Liam','Bruna','liam@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','20525560-5');
INSERT INTO "bibliotecario" VALUES (22,'Nicolas','Perez','nicolas@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12354458-5');
INSERT INTO "bibliotecario" VALUES (23,'Karla','Angel','karla@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','13216245-k');
INSERT INTO "bibliotecario" VALUES (24,'Karolain','Cabrera','karolain@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12548879-3');
INSERT INTO "bibliotecario" VALUES (25,'Matias','Franjola','matias@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12545635-5');
INSERT INTO "bibliotecario" VALUES (26,'Marta','Flores','marta@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12545878-9');
INSERT INTO "bibliotecario" VALUES (27,'Hernan','Bruna','hernan@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','13293758-3');
COMMIT;
