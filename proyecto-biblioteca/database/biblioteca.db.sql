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
	FOREIGN KEY("ID_E") REFERENCES "ejemplar"("ID_E"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P"),
	PRIMARY KEY("ID_E","ID_P")
);
CREATE TABLE IF NOT EXISTS "escribe" (
	"ID_A"	INTEGER NOT NULL,
	"ID_L"	INTEGER NOT NULL,
	FOREIGN KEY("ID_A") REFERENCES "autor"("ID_A"),
	FOREIGN KEY("ID_L") REFERENCES "libro"("ID_L"),
	PRIMARY KEY("ID_A","ID_L")
);
CREATE TABLE IF NOT EXISTS "pide" (
	"ID_U"	INTEGER NOT NULL,
	"ID_P"	INTEGER NOT NULL,
	PRIMARY KEY("ID_U","ID_P"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P"),
	FOREIGN KEY("ID_U") REFERENCES "usuario"("ID_U")
);
CREATE TABLE IF NOT EXISTS "registra" (
	"ID_P"	INTEGER NOT NULL,
	"ID_B"	INTEGER NOT NULL,
	PRIMARY KEY("ID_P","ID_B"),
	FOREIGN KEY("ID_P") REFERENCES "prestamo_temp"("ID_P"),
	FOREIGN KEY("ID_B") REFERENCES "bibliotecario"("ID_B")
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"ID_U"	INTEGER,
	"NOMBRE_U"	TEXT,
	"APELLIDO_U"	TEXT,
	"DIRECCION_U"	TEXT,
	"RUT_U"	TEXT NOT NULL,
	"CELULAR_U"	INTEGER,
	"CORREO_U"	TEXT,
	"TIPO_U"	TEXT,
	PRIMARY KEY("ID_U" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "libro" (
	"ID_L"	INTEGER,
	"ISBN"	VARHCAR NOT NULL,
	"TITULO"	TEXT NOT NULL,
	"NUMERO_PAGINAS"	INTEGER,
	"STOCK"	INTEGER NOT NULL,
	PRIMARY KEY("ID_L" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "bibliotecario" (
	"ID_B"	INTEGER,
	"NOMBRE_B"	TEXT,
	"APELLIDO_B"	TEXT,
	"CORREO_B"	VARCHAR NOT NULL,
	"CONTRASENA"	VARCHAR(100) NOT NULL,
	"RUT_B"	TEXT,
	"CELULAR_B"	TEXT,
	PRIMARY KEY("ID_B" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ejemplar" (
	"ID_E"	INTEGER,
	"ID_L"	INTEGER,
	"ISBN"	VARCHAR(20),
	"Estado"	VARCHAR(20),
	PRIMARY KEY("ID_E" AUTOINCREMENT),
	FOREIGN KEY("ID_L") REFERENCES "libro"("ID_L")
);
CREATE TABLE IF NOT EXISTS "prestamo" (
	"ID_P"	INTEGER,
	"RUT_U"	TEXT NOT NULL,
	"ISBN"	INTEGER NOT NULL,
	"F_PRESTAMO"	TEXT NOT NULL,
	"F_DEVOLUCION"	TEXT NOT NULL,
	"TIPO_U"	TEXT NOT NULL,
	"ID_B"	INTEGER,
	"RENOVADO"	INTEGER,
	PRIMARY KEY("ID_P" AUTOINCREMENT),
	FOREIGN KEY("ID_B") REFERENCES "bibliotecario"("ID_B")
);
INSERT INTO "usuario" VALUES (1,'Emerson de Jesus','Ilaja','Granaderos 3250','13.293.245-k',923548776,'ilaja@example.com','Docente');
INSERT INTO "usuario" VALUES (4,'John','Selti','Granaderos 2350','21.480.695-9',923541254,'selti@example.com','Alumno');
INSERT INTO "usuario" VALUES (6,'Liam','Bruna','Granaderos 3250','20.525.560-5',923999895,'bruna@example.com','Alumno');
INSERT INTO "libro" VALUES (3,'l-001','The Last Of Us',200,9);
INSERT INTO "libro" VALUES (4,'l-002','To Kill a Mockingbird',281,10);
INSERT INTO "libro" VALUES (5,'l-003','The Great Gatsby',180,5);
INSERT INTO "libro" VALUES (6,'l-004','1984',328,3);
INSERT INTO "libro" VALUES (7,'l-005','Where the Wild Things Are',48,8);
INSERT INTO "libro" VALUES (8,'l-006','Charlottes Web',192,6);
INSERT INTO "libro" VALUES (9,'l-007','Holes',233,4);
INSERT INTO "libro" VALUES (10,'l-008','Harry Potter and the Sorcerers Stone',309,7);
INSERT INTO "libro" VALUES (11,'l-009','The Hunger Games',374,9);
INSERT INTO "libro" VALUES (12,'l-010','The Hobbit',320,2);
INSERT INTO "libro" VALUES (13,'l-011','The Fault in Our Stars',313,5);
INSERT INTO "libro" VALUES (14,'l-012','The Chronicles of Narnia',767,8);
INSERT INTO "libro" VALUES (15,'l-013','The Alchemist',197,3);
INSERT INTO "libro" VALUES (16,'l-014','Pride and Prejudice',279,10);
INSERT INTO "libro" VALUES (17,'l-015','The Book Thief',552,6);
INSERT INTO "bibliotecario" VALUES (21,'Liam','Bruna','liam@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','20525560-5','+56 923999895');
INSERT INTO "bibliotecario" VALUES (22,'Nicolas','Perez','nicolas@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12354458-5',NULL);
INSERT INTO "bibliotecario" VALUES (23,'Karla','Angel','karla@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','13216245-k',NULL);
INSERT INTO "bibliotecario" VALUES (24,'Karolain','Cabrera','karolain@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12548879-3',NULL);
INSERT INTO "bibliotecario" VALUES (25,'Matias','Franjola','matias@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12545635-5',NULL);
INSERT INTO "bibliotecario" VALUES (26,'Marta','Flores','marta@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','12545878-9',NULL);
INSERT INTO "bibliotecario" VALUES (27,'Hernan','Bruna','hernan@example.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','13293758-3',NULL);
INSERT INTO "ejemplar" VALUES (1,3,'l-001','BUENO');
INSERT INTO "ejemplar" VALUES (2,5,'l-003','BUENO');
INSERT INTO "ejemplar" VALUES (3,6,'l-004','BUENO');
INSERT INTO "ejemplar" VALUES (4,7,'l-005','BUENO');
INSERT INTO "ejemplar" VALUES (5,4,'l-002','BUENO');
INSERT INTO "ejemplar" VALUES (6,8,'l-006','BUENO');
INSERT INTO "ejemplar" VALUES (7,9,'l-007','BUENO');
INSERT INTO "ejemplar" VALUES (8,10,'l-008','BUENO');
INSERT INTO "ejemplar" VALUES (9,11,'l-009','BUENO');
INSERT INTO "ejemplar" VALUES (10,12,'l-0010','BUENO');
INSERT INTO "ejemplar" VALUES (11,13,'l-0011','BUENO');
INSERT INTO "ejemplar" VALUES (12,14,'l-0012','BUENO');
INSERT INTO "ejemplar" VALUES (13,15,'l-0013','BUENO');
INSERT INTO "ejemplar" VALUES (14,16,'l-0014','BUENO');
INSERT INTO "ejemplar" VALUES (15,17,'l-0015','BUENO');
INSERT INTO "prestamo" VALUES (26,'20.525.560-5','l-001','2023-07-03','2023-07-10','Alumno',21,NULL);
COMMIT;
