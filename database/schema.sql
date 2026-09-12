CREATE TABLE IF NOT EXISTS usuarios_sistema (
	"id_usuario"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"contrasena"	TEXT NOT NULL,
	"rol_id"	INTEGER NOT NULL,
	"activa"	INTEGER,
	PRIMARY KEY("id_usuario" AUTOINCREMENT),
	FOREIGN KEY ("rol_id")
		REFERENCES roles("id_rol")
);

CREATE TABLE IF NOT EXISTS citas (
	"id_cita"	INTEGER,
	"fecha"	TEXT NOT NULL,
	"hora"	TEXT,
	"estado_id"	INTEGER,
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

CREATE TABLE IF NOT EXISTS domicilio_estatus (
	"id_domicilio_estatus"	INTEGER,
	"domicilio_estatus"	TEXT NOT NULL,
	PRIMARY KEY("id_domicilio_estatus" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS direcciones (
	"id_direccion"	INTEGER,
	"calle_numero"	TEXT NOT NULL,
	"colonia"	TEXT NOT NULL,
	"municipio"	TEXT NOT NULL,
	"domicilio_estatus_id"	INTEGER,
	PRIMARY KEY("id_direccion" AUTOINCREMENT),
	FOREIGN KEY ("domicilio_estatus_id")
		REFERENCES domicilio_estatus("id_domicilio_estatus")
);

CREATE TABLE IF NOT EXISTS usuarias_direcciones (
	"usuaria_id"	INTEGER,
	"direccion_id"	INTEGER,
	FOREIGN KEY ("usuaria_id")
		REFERENCES usuarias("id_usuaria"),
	FOREIGN KEY ("direccion_id")
		REFERENCES direcciones("id_direccion")
);

CREATE TABLE IF NOT EXISTS escolaridades (
	"id_escolaridad"	INTEGER,
	"escolaridad"	TEXT NOT NULL,
	PRIMARY KEY("id_escolaridad" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS estados_civiles (
	"id_estado_civil"	INTEGER,
	"estado_civil"	TEXT NOT NULL,
	PRIMARY KEY("id_estado_civil" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS sexos (
	"id_sexo"	INTEGER,
	"sexo"	TEXT NOT NULL,
	PRIMARY KEY("id_sexo" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS lenguas_indigenas (
	"id_lengua_indigena"	INTEGER,
	"lengua_indigena"	TEXT NOT NULL,
	PRIMARY KEY("id_lengua_indigena" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS servicios_immujer (
	"id_servicio_immujer"	INTEGER,
	"servicio_immujer"	TEXT NOT NULL,
	PRIMARY KEY("id_servicio_immujer" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS usuarias (
	"id_usuaria"				INTEGER,
	"nombre"					TEXT NOT NULL,
	"edad"						INTEGER,
	"telefono"					TEXT UNIQUE NOT NULL,
	"fecha_nacimiento"			TEXT,
	"lugar_nacimiento"			TEXT,
	"escolaridad_id"			INTEGER,
	"ocupacion"					TEXT,
	"estado_civil_id"			INTEGER,
	"sexo_id"					INTEGER,
	"lengua_indigena_id"		INTEGER,
	"padecimiento"				TEXT,
	"servicio_immujer_id"		INTEGER,
	"servicio_immujer_fecha"	TEXT,
	"terapia_tiempo"			TEXT,
	"terapia_lugar"				TEXT,
	"canalizada_por"			TEXT,
	"red_apoyo"					TEXT,
	"motivo_consulta"			TEXT,
	"estatus_id"				INTEGER,
	PRIMARY KEY("id_usuaria" AUTOINCREMENT),
	FOREIGN KEY ("escolaridad_id")
		REFERENCES escolaridades("id_escolaridad"),
	FOREIGN KEY ("estado_civil_id")
		REFERENCES estados_civiles("id_estado_civil"),
	FOREIGN KEY ("sexo_id")
		REFERENCES sexos("id_sexo"),
	FOREIGN KEY ("lengua_indigena_id")
		REFERENCES lenguas_indigenas("id_lengua_indigena"),
	FOREIGN KEY ("servicio_immujer_id")
		REFERENCES servicios_immujer("id_servicio_immujer"),
	FOREIGN KEY ("estatus_id")
		REFERENCES estatus("id_estatus")
);

CREATE TABLE IF NOT EXISTS estados_cita (
    id_estado_cita INTEGER PRIMARY KEY AUTOINCREMENT,
    estado_cita TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dependencias (
    id_dependencia INTEGER PRIMARY KEY AUTOINCREMENT,
    dependencia TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS agresores (
    "id_agresor"          INTEGER,
    "nombre_agresor"      TEXT    NOT NULL,
    "parentesco_agresor"  TEXT,
    "ocupacion_agresor"   TEXT,
    "edad_agresor"        INTEGER,
    PRIMARY KEY("id_agresor" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS usuarias_agresores (
    "usuaria_id"  INTEGER NOT NULL,
    "agresor_id"  INTEGER NOT NULL,
    FOREIGN KEY ("usuaria_id") 
		REFERENCES usuarias("id_usuaria"),
    FOREIGN KEY ("agresor_id") 
		REFERENCES agresores("id_agresor")
);

CREATE TABLE IF NOT EXISTS usuarias_inasistencias (
	"usuaria_id"	INTEGER NOT NULL,
	"inasistencias"	INTEGER NOT NULL,
	FOREIGN KEY ("usuaria_id")
		REFERENCES usuarias("id_usuaria")
);

-- CATÁLOGOS

-- domicilio_estatus
INSERT OR IGNORE INTO domicilio_estatus (domicilio_estatus) VALUES
('Propio'),
('Rentado'),
('Prestado');

-- escolaridades
INSERT OR IGNORE INTO escolaridades (escolaridad) VALUES
('Ninguna'),
('Primaria'),
('Secundaria'),
('Bachillerato'),
('Licenciatura'),
('Posgrado');

-- estados_civiles
INSERT OR IGNORE INTO estados_civiles (estado_civil) VALUES
('Soltera'),
('Casada'),
('Divorciada'),
('Viuda'),
('Unión libre');

-- sexos
INSERT OR IGNORE INTO sexos (sexo) VALUES
('Femenino'),
('Masculino'),
('Otro');

-- lenguas_indigenas
INSERT OR IGNORE INTO lenguas_indigenas (lengua_indigena) VALUES
('Ninguna'),
('Mixteco'),
('Zapoteco'),
('Mazateco'),
('Otra');

-- servicios_immujer
INSERT OR IGNORE INTO servicios_immujer (servicio_immujer) VALUES
('Psicológico'),
('Jurídico');

-- estatus
INSERT OR IGNORE INTO estatus (estatus) VALUES
('Activa'),
('Inactiva');

-- estados cita
INSERT OR IGNORE INTO estados_cita (estado_cita) VALUES
('Programada'),
('Atendida'),
('Cancelada'),
('No asistió');

-- roles
INSERT OR IGNORE INTO roles (rol) VALUES
('Administrador'),
('Psicologa');

-- dependencias
INSERT OR IGNORE INTO dependencias (dependencia) VALUES
('Ninguna'),
('Vicefiscalía'),
('Juzgado familiar'),
('Hospital'),
('Otra');