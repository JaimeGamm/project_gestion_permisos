DROP DATABASE IF EXISTS gestion_permisos_2db;
CREATE DATABASE gestion_permisos_2db;
USE gestion_permisos_2db;

-- Crear la tabla de usuarios
	CREATE TABLE usuarios (
		id_usuario INT AUTO_INCREMENT PRIMARY KEY,
		nombre VARCHAR(100),
		email VARCHAR(100) UNIQUE,
		password VARCHAR(100),
		rol ENUM('administrador', 'empleado') NOT NULL,
		fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);

	-- Crear la tabla de permisos
		CREATE TABLE permisos (
			id_permiso INT AUTO_INCREMENT PRIMARY KEY,
			id_usuario INT,  -- Usuario que solicita el permiso
			tipo_permiso ENUM('salud', 'familiar', 'otros') NOT NULL,
			descripcion TEXT,  -- Motivo detallado del permiso
			fecha_permiso DATE NOT NULL,
			hora_inicio TIME NOT NULL,
			hora_fin TIME NOT NULL,
			estado ENUM('pendiente', 'aprobado', 'rechazado', 'cancelado') DEFAULT 'pendiente',
			id_admin INT DEFAULT NULL,  -- Administrador que gestionó el permiso
			fecha_revision TIMESTAMP DEFAULT NULL,  -- Fecha de revisión del admin
			comentarios_admin TEXT,  -- Comentarios del admin
			fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
			FOREIGN KEY (id_admin) REFERENCES usuarios(id_usuario)
		);

	-- Crear la tabla de historial de permisos
	CREATE TABLE historial_permisos (
		id_historial INT AUTO_INCREMENT PRIMARY KEY,
		id_permiso INT,  -- El permiso asociado al historial
		id_usuario INT,  -- Usuario (admin o empleado) que realizó la acción
		accion ENUM('solicitud', 'aprobado', 'rechazado', 'cancelado') NOT NULL,
		fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		comentario TEXT,
		FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso),
		FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
	);


-- Administradores
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Carlos Pérez', 'carlos.admin@empresa.com', 'password123', 'administrador'),
('Ana Rodríguez', 'ana.admin@empresa.com', 'admin456nombre', 'administrador');

-- Empleados
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Laura Gómez', 'laura.gomez@empresa.com', 'empleado123', 'empleado'),
('José Martínez', 'jose.martinez@empresa.com', 'empleado456', 'empleado'),
('María Torres', 'maria.torres@empresa.com', 'empleado789', 'empleado');


-- Permisos solicitados por los empleados
INSERT INTO permisos (id_usuario, tipo_permiso, descripcion, fecha_permiso, hora_inicio, hora_fin, estado) VALUES
(3, 'salud', 'Cita médica', '2024-09-20', '09:00:00', '12:00:00', 'pendiente'),
(4, 'familiar', 'Asistencia a una reunión familiar', '2024-09-22', '14:00:00', '18:00:00', 'pendiente'),
(5, 'otros', 'Trámite bancario importante', '2024-09-21', '10:00:00', '12:00:00', 'pendiente');


-- Historial de acciones en permisos (solicitudes realizadas)
INSERT INTO historial_permisos (id_permiso, id_usuario, accion, comentario) VALUES
(1, 3, 'solicitud', 'Solicitud de permiso por cita médica'),
(2, 4, 'solicitud', 'Solicitud de permiso para una reunión familiar'),
(3, 5, 'solicitud', 'Solicitud de permiso para un trámite bancario');

-- Aprobación de un permiso por un administrador
INSERT INTO historial_permisos (id_permiso, id_usuario, accion, comentario) VALUES
(1, 1, 'aprobado', 'Aprobado por Carlos Pérez: permiso para cita médica');


SELECT p.id_permiso, u.nombre, p.tipo_permiso, p.descripcion, p.fecha_permiso, p.hora_inicio, p.hora_fin
FROM permisos p
JOIN usuarios u ON p.id_usuario = u.id_usuario
WHERE p.estado = 'pendiente';

select * from usuarios;

USE gestion_permisos_2db;
select * from permisos;
SELECT MONTH(fecha_solicitud) AS mes, COUNT(id_permiso) AS total_permisos
	FROM permisos
	WHERE YEAR(fecha_solicitud) = YEAR(CURRENT_DATE)
	GROUP BY mes
	ORDER BY mes;
    
	SELECT id_permiso, fecha_solicitud
	FROM permisos
	WHERE YEAR(fecha_solicitud) = YEAR(CURRENT_DATE);

SELECT MONTH(fecha_solicitud) AS mes, COUNT(id_permiso) AS total_permisos
FROM permisos
WHERE YEAR(fecha_solicitud) = YEAR(CURRENT_DATE)
GROUP BY mes
ORDER BY mes;


-- Permisos solicitados por los empleados en diferentes meses
INSERT INTO permisos (id_usuario, tipo_permiso, descripcion, fecha_permiso, hora_inicio, hora_fin, estado) VALUES
-- Enero
(3, 'salud', 'Cita médica de control', '2024-01-15', '10:00:00', '12:00:00', 'aprobado'),
(4, 'familiar', 'Evento familiar importante', '2024-01-20', '15:00:00', '19:00:00', 'pendiente'),

-- Febrero
(5, 'otros', 'Renovación de pasaporte', '2024-02-05', '09:00:00', '11:00:00', 'aprobado'),
(3, 'familiar', 'Reunión escolar de hijos', '2024-02-12', '13:00:00', '15:00:00', 'pendiente'),

-- Marzo
(4, 'salud', 'Chequeo médico anual', '2024-03-10', '09:00:00', '11:30:00', 'aprobado'),
(5, 'otros', 'Visita a notaría', '2024-03-25', '10:00:00', '12:00:00', 'pendiente'),

-- Abril
(3, 'salud', 'Vacunación', '2024-04-08', '11:00:00', '13:00:00', 'aprobado'),
(5, 'otros', 'Revisión de contrato', '2024-04-22', '14:00:00', '16:00:00', 'pendiente'),

-- Mayo
(4, 'familiar', 'Evento escolar de hijos', '2024-05-18', '09:00:00', '12:00:00', 'pendiente'),
(3, 'otros', 'Trámite personal en el banco', '2024-05-30', '11:00:00', '13:00:00', 'aprobado'),

-- Junio
(5, 'familiar', 'Asistencia a boda de familiar', '2024-06-15', '16:00:00', '20:00:00', 'pendiente'),
(4, 'otros', 'Consulta legal en la tarde', '2024-06-23', '14:00:00', '16:30:00', 'aprobado'),

-- Julio
(3, 'salud', 'Cita médica odontológica', '2024-07-05', '09:30:00', '11:00:00', 'aprobado'),
(4, 'otros', 'Inscripción de documentos personales', '2024-07-22', '10:00:00', '12:00:00', 'pendiente'),

-- Agosto
(5, 'salud', 'Consulta con especialista', '2024-08-10', '14:00:00', '16:00:00', 'pendiente'),
(3, 'familiar', 'Reunión familiar', '2024-08-25', '17:00:00', '21:00:00', 'aprobado'),

-- Septiembre
(3, 'salud', 'Cita médica', '2024-09-20', '09:00:00', '12:00:00', 'pendiente'),
(4, 'familiar', 'Asistencia a una reunión familiar', '2024-09-22', '14:00:00', '18:00:00', 'pendiente'),
(5, 'otros', 'Trámite bancario importante', '2024-09-21', '10:00:00', '12:00:00', 'pendiente'),

-- Octubre
(4, 'salud', 'Chequeo de salud preventiva', '2024-10-13', '11:00:00', '13:30:00', 'aprobado'),
(3, 'otros', 'Asesoría financiera', '2024-10-28', '09:00:00', '11:00:00', 'pendiente'),

-- Noviembre
(5, 'familiar', 'Viaje familiar corto', '2024-11-05', '10:00:00', '18:00:00', 'aprobado'),
(4, 'otros', 'Consulta jurídica', '2024-11-19', '14:00:00', '17:00:00', 'pendiente'),

-- Diciembre
(3, 'salud', 'Cita de chequeo general', '2024-12-09', '09:00:00', '11:00:00', 'pendiente'),
(5, 'otros', 'Visita a consulado', '2024-12-15', '13:00:00', '16:00:00', 'pendiente');


SELECT MONTH(fecha_permiso) AS mes, COUNT(id_permiso) AS total_permisos
FROM permisos
WHERE YEAR(fecha_permiso) = YEAR(CURRENT_DATE)
GROUP BY mes
ORDER BY mes;


        SELECT u.nombre AS admin, 
               SUM(CASE WHEN p.estado = 'aprobado' THEN 1 ELSE 0 END) AS aprobaciones,
               SUM(CASE WHEN p.estado = 'rechazado' THEN 1 ELSE 0 END) AS rechazos
        FROM permisos p
        JOIN usuarios u ON p.id_admin = u.id_usuario
        WHERE p.estado IN ('aprobado', 'rechazado')
        GROUP BY u.nombre;