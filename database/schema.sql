CREATE TABLE IF NOT EXISTS usuarias (
	"id_usuaria"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"fecha_ingreso"	TEXT NOT NULL,
	"colonia"	TEXT,
	"edad"	INTEGER,
	"telefono"	TEXT UNIQUE,
	"problematica"	INTEGER,
	"estatus_id"	INTEGER,
	PRIMARY KEY("id_usuaria" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS usuarios_sistema (
	"id_usuario"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"contrasena"	TEXT NOT NULL,
	"rol_id"	INTEGER NOT NULL,
	"activa"	INTEGER,
	PRIMARY KEY("id_usuario" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS citas (
	"id_cita"	INTEGER,
	"fecha"	TEXT NOT NULL,
	"hora"	TEXT,
	"estado"	TEXT,
	"usuaria_id"	INTEGER NOT NULL,
	"psicologa_id"	INTEGER NOT NULL,
	PRIMARY KEY("id_cita" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS estatus (
	"id_estatus"	INTEGER,
	"estatus"	TEXT NOT NULL,
	PRIMARY KEY("id_estatus" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS notificaciones (
	"id_notificacion"	INTEGER,
	"fecha_envio"	TEXT NOT NULL,
	"mensaje"	TEXT,
	"cita_id"	INTEGER NOT NULL,
	PRIMARY KEY("id_notificacion" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS psicologas (
	"id_psicologas"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"especialidad"	TEXT,
	"horario"	TEXT,
	"activa"	INTEGER,
	PRIMARY KEY("id_psicologas" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS roles (
	"id_rol"	INTEGER,
	"rol"	TEXT NOT NULL,
	PRIMARY KEY("id_rol" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS sesiones (
	"id_sesion"	INTEGER,
	"fecha_sesion"	TEXT,
	"observaciones"	TEXT,
	"cita_id"	INTEGER,
    PRIMARY KEY("id_sesion" AUTOINCREMENT)
);