-- Partimos de un entorno limpio
DROP DATABASE IF EXISTS clinica_capilar;

-- Comprobamos el character set y el collation del server
SHOW VARIABLES
WHERE Variable_name IN ('character_set_server', 'collation_server');


-- Creamos la base de datos especificando de forma explicita el conjunto de caracteres y la collation
-- que en este caso son los mismos que los valores por defecto del server
CREATE DATABASE clinica_capilar
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Seleccionamos la base de datos
USE clinica_capilar;

-- Comprobamos que estamos en la base de datos
SELECT DATABASE();

-- Validamos que se ha creado con el caracter set y la collation
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'clinica_capilar';


-- Creación de tablas de la base de datos
SELECT '1. Crear las tablas y sus relaciones.' as ejercicio;

CREATE TABLE pacientes (
    id_paciente INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero ENUM('F', 'M', 'O') NOT NULL,
    historial_medico TEXT,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    fecha_alta DATE NOT NULL
);

CREATE TABLE personal_medico (
    id_medico INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especialidad ENUM('Cirugia', 'Dermatologia', 'Enfermeria', 'Asistente', 'Otros') NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20)
);

CREATE TABLE catalogo_medicamentos (
    id_medicamento INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE facturas (
    id_factura INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    fecha_factura DATETIME NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    pagado BOOL NOT NULL DEFAULT FALSE,
    detalle_transaccion VARCHAR(255),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT
);

CREATE TABLE citas (
    id_cita INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_factura INT NOT NULL UNIQUE,
    fecha_cita DATETIME NOT NULL,
    motivo VARCHAR(255),
    confirmada BOOL NOT NULL DEFAULT FALSE,
    observaciones TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE RESTRICT
);

CREATE TABLE trasplantes (
    id_operacion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    id_factura INT NOT NULL UNIQUE,
    fecha_operacion DATETIME NOT NULL,
    tipo_procedimiento VARCHAR(100) NOT NULL,
    zona_donante VARCHAR(100),
    zona_receptora VARCHAR(100),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE RESTRICT
);

CREATE TABLE equipo_operacion (
    id_operacion INT NOT NULL,
    id_medico INT NOT NULL,
    rol ENUM('Responsable', 'Asistente') NOT NULL,
    PRIMARY KEY (id_operacion, id_medico),
    FOREIGN KEY (id_operacion) REFERENCES trasplantes(id_operacion) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT
);

CREATE TABLE tratamientos (
    id_tratamiento INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_factura INT NULL,
    id_medicamento INT NULL,
    dosis VARCHAR(50),
    frecuencia VARCHAR(50),
    indicaciones TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE SET NULL,
    FOREIGN KEY (id_medicamento) REFERENCES catalogo_medicamentos(id_medicamento) ON DELETE SET NULL
);

CREATE TABLE visitas_seguimiento (
    id_visita INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha_visita DATETIME NOT NULL,
    observaciones TEXT,
    resultados VARCHAR(255),
    recomendaciones TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT
);

CREATE TABLE documentacion (
    id_documento INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    tipo_documento VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ruta_archivo VARCHAR(255) NOT NULL,
    fecha_documento DATE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE
);

SELECT 'Tablas creadas correctamente.' as resultado;


-- Generamos mock data para las tablas
SELECT '2. Insertar datos en cada una de las tablas.' as ejercicio;

INSERT INTO pacientes (id_paciente, nombre, fecha_nacimiento, genero, historial_medico, email, telefono, fecha_alta) VALUES
(1, 'Carlos Ramirez', '1985-05-15', 'M', 'Hipertensión controlada', 'carlos.r@email.com', '+34611223344', '2023-01-10'),
(2, 'Ana García', '1992-11-20', 'F', 'Sin alergias conocidas', 'ana.g@email.com', '+34622334455', '2023-02-05'),
(3, 'Javier Fernandez', '1978-03-30', 'M', 'Alergia a la penicilina', 'javier.f@email.com', '+34633445566', '2023-03-12'),
(4, 'Luis Suarez', '1980-08-22', 'M', 'Ninguno', 'luis.s@email.com', '+34644556677', '2023-04-01'),
(5, 'Maria Gomez', '1995-12-10', 'F', 'Anemia leve (ferropénica)', 'maria.g@email.com', '+34655667788', '2023-05-15');

INSERT INTO personal_medico (id_medico, nombre, especialidad, email, telefono) VALUES
(1, 'Dr. Alejandro Vega', 'Cirugia', 'dr.vega@clinicacapilar.com', '+34911112233'),
(2, 'Dra. Laura Montes', 'Dermatologia', 'dra.montes@clinicacapilar.com', '+34912223344'),
(3, 'Enf. Sofia Nieto', 'Enfermeria', 'sofia.nieto@clinicacapilar.com', '+34913334455'),
(4, 'Dr. Pedro Lillo', 'Asistente', 'dr.lillo@clinicacapilar.com', '+34914445566');

INSERT INTO catalogo_medicamentos (id_medicamento, nombre) VALUES
(1, 'Minoxidil 5%'),
(2, 'Finasteride 1mg'),
(3, 'Biotina Complex'),
(4, 'Dutasteride 0.5mg'),
(5, 'Ketoconazol 2% Champú'),
(6, 'Multivitaminas Capilares');

INSERT INTO facturas (id_factura, id_paciente, fecha_factura, concepto, monto, pagado, detalle_transaccion) VALUES
(1, 1, '2023-01-10 10:30:00', 'Consulta inicial de valoración', 100.00, TRUE, 'Pago con tarjeta'),
(2, 2, '2023-02-05 12:00:00', 'Consulta inicial de valoración', 100.00, TRUE, 'Pago con tarjeta'),
(3, 3, '2023-03-12 16:15:00', 'Consulta inicial de valoración', 100.00, TRUE, 'Pago en efectivo'),
(4, 1, '2023-04-20 09:00:00', 'Trasplante capilar FUE 2500 UFs', 4500.00, TRUE, 'Transferencia bancaria'),
(5, 2, '2023-06-15 11:45:00', 'Sesión de Plasma Rico en Plaquetas (PRP)', 250.00, FALSE, 'Pendiente de pago'),
(6, 4, '2023-04-01 10:30:00', 'Consulta inicial de valoración', 100.00, TRUE, 'Pago con tarjeta'),
(7, 5, '2023-05-15 11:00:00', 'Consulta por caída reaccional', 80.00, TRUE, 'Efectivo'),
(8, 3, '2023-06-10 08:30:00', 'Trasplante DHI 1500 UFs', 3200.00, TRUE, 'Financiado a 12 meses'),
(9, 4, '2023-04-15 10:00:00', 'Sesión de Mesoterapia Capilar', 150.00, TRUE, 'Tarjeta de crédito');

INSERT INTO citas (id_cita, id_paciente, id_medico, id_factura, fecha_cita, motivo, confirmada, observaciones) VALUES
(1, 1, 2, 1, '2023-01-10 10:00:00', 'Valoración de alopecia androgenética', TRUE, 'Paciente presenta patrón Norwood IV.'),
(2, 2, 2, 2, '2023-02-05 11:30:00', 'Consulta por caída de cabello postparto', TRUE, 'Efluvio telógeno, se recomienda tratamiento.'),
(3, 3, 1, 3, '2023-03-12 16:00:00', 'Segunda opinión sobre trasplante previo', TRUE, 'Se evalúan opciones para densificar coronilla.'),
(4, 4, 1, 6, '2023-04-01 10:00:00', 'Valoración para posible injerto', TRUE, 'Zona donante excelente. Apto para intervención.'),
(5, 5, 2, 7, '2023-05-15 10:30:00', 'Consulta por pérdida difusa', TRUE, 'Se manda analítica completa para descartar déficit de hierro.');

INSERT INTO trasplantes (id_operacion, id_paciente, id_factura, fecha_operacion, tipo_procedimiento, zona_donante, zona_receptora) VALUES
(1, 1, 4, '2023-04-20 09:00:00', 'FUE Zafiro', 'Occipital y laterales', 'Frontal y coronilla'),
(2, 3, 8, '2023-06-10 08:00:00', 'DHI Implanters', 'Occipital', 'Coronilla');

INSERT INTO equipo_operacion (id_operacion, id_medico, rol) VALUES
(1, 1, 'Responsable'),
(1, 3, 'Asistente'),
(2, 1, 'Responsable'),
(2, 4, 'Asistente'),
(2, 3, 'Asistente');

INSERT INTO tratamientos (id_tratamiento, id_paciente, id_medico, id_factura, id_medicamento, dosis, frecuencia, indicaciones, fecha_inicio, fecha_fin) VALUES
(1, 1, 1, NULL, NULL, NULL, NULL, 'Cuidados post-operatorios: Lavados suaves con suero y reposo relativo.', '2023-04-20', NULL),
(2, 2, 2, NULL, 1, '1 ml', '2 veces al día', 'Aplicar en cuero cabelludo seco mediante masajes.', '2023-02-06', '2024-02-06'),
(3, 2, 2, 5, NULL, NULL, NULL, 'Tratamiento de bioestimulación capilar (PRP).', '2023-06-15', '2023-09-15'),
(4, 3, 1, NULL, 2, '1 comprimido', '1 vez al día', 'Tomar con la cena de forma ininterrumpida.', '2023-03-13', NULL),
(5, 4, 2, 9, 4, 'Microinyecciones', '1 sesión mensual', 'Mesoterapia capilar antiandrógena.', '2023-04-15', '2023-07-15'),
(6, 5, 2, NULL, 5, 'Dosis habitual', '3 veces por semana', 'Dejar actuar 5 minutos antes de aclarar.', '2023-05-15', '2023-08-15');

INSERT INTO visitas_seguimiento (id_visita, id_paciente, id_medico, fecha_visita, observaciones, resultados, recomendaciones) VALUES
(1, 1, 1, '2023-10-25 12:30:00', 'Revisión a los 6 meses del trasplante.', 'Crecimiento del 70% del cabello implantado. Sin signos de infección.', 'Continuar con cuidados y valorar inicio de Minoxidil para mantenimiento.'),
(2, 2, 2, '2023-08-10 10:00:00', 'Seguimiento del tratamiento para efluvio telógeno.', 'Notable disminución de la caída y aparición de nuevo cabello.', 'Mantener tratamiento con Minoxidil y suplementos. Próxima revisión en 6 meses.'),
(3, 3, 1, '2023-12-10 16:30:00', 'Revisión a los 6 meses post-DHI.', 'Crecimiento excelente, densidad muy natural en la coronilla.', 'Dar el alta quirúrgica y pasar a revisiones anuales.'),
(4, 4, 2, '2023-05-15 10:00:00', 'Control post primera sesión de mesoterapia.', 'Leve enrojecimiento que remitió en 2 horas, paciente sin dolor.', 'Continuar con las sesiones mensuales programadas.');

INSERT INTO documentacion (id_documento, id_paciente, tipo_documento, descripcion, ruta_archivo, fecha_documento) VALUES
(1, 1, 'Consentimiento Informado', 'Consentimiento firmado para la intervención FUE.', '/docs/pac_1/consent_fue_20230419.pdf', '2023-04-19'),
(2, 1, 'Fotografías Pre-operatorias', 'Set de 5 fotografías antes de la intervención.', '/docs/pac_1/fotos_preop_20230419.zip', '2023-04-19'),
(3, 2, 'Analítica Sanguínea', 'Resultados de analítica general.', '/docs/pac_2/analitica_20230201.pdf', '2023-02-01'),
(4, 3, 'Fotografías Pre-operatorias', 'Fotos detalle de la coronilla previas a técnica DHI.', '/docs/pac_3/fotos_dhi_pre.zip', '2023-06-09'),
(5, 5, 'Analítica Completa', 'Analítica para descartar deficiencias de hierro o problemas de tiroides.', '/docs/pac_5/analitica_completa.pdf', '2023-05-15');


SELECT 'Datos insertados correctamente.' as resultado;


-- Querys
SELECT '3. SELECT de los datos de cada tabla.' as ejercicio;

SELECT * FROM pacientes;
SELECT * FROM personal_medico;
SELECT * FROM catalogo_medicamentos;
SELECT * FROM facturas;
SELECT * FROM citas;
SELECT * FROM trasplantes;
SELECT * FROM equipo_operacion;
SELECT * FROM tratamientos;
SELECT * FROM visitas_seguimiento;
SELECT * FROM documentacion;

-- Trasplantes identificando al paciente y al equipo médico
SELECT '4. Trasplantes identificando al paciente y al equipo médico.' as ejercicio;

SELECT
	m.nombre as medico,
	e.rol,
	p.nombre as paciente,
	t.fecha_operacion,
	t.zona_receptora,
	t.zona_donante
FROM trasplantes t
INNER JOIN pacientes p
ON t.id_paciente = p.id_paciente
INNER JOIN equipo_operacion e
ON t.id_operacion = e.id_operacion
INNER JOIN personal_medico m
ON e.id_medico = m.id_medico;

-- Agrupando al equipo médico en un mismo registro
-- Ver: https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html#function_group-concat
SELECT '5. Agrupando al equipo médico en un mismo registro.' as ejercicio;

SELECT
	GROUP_CONCAT(CONCAT(m.nombre, ' [', e.rol, ']')
	 			ORDER BY e.rol, m.nombre SEPARATOR ', ') AS personal_medico,
	p.nombre AS paciente,
	t.fecha_operacion,
	t.zona_receptora,
	t.zona_donante
FROM trasplantes t
INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
INNER JOIN equipo_operacion e ON t.id_operacion = e.id_operacion
INNER JOIN personal_medico m ON e.id_medico = m.id_medico
GROUP BY p.nombre, t.fecha_operacion, t.zona_receptora, t.zona_donante;

-- Trazabilidad de las facturas que corresponden a trasplantes
-- Ver: https://dev.mysql.com/doc/refman/8.4/en/exists-and-not-exists-subqueries.html
SELECT '6. Trazabilidad de las facturas que corresponder a trasplantes' as ejercicio;

SELECT f.* FROM facturas f
WHERE EXISTS (SELECT * FROM trasplantes t
			  WHERE t.fecha_operacion BETWEEN f.fecha_factura - INTERVAL 1 HOUR
										  AND f.fecha_factura + INTERVAL 1 HOUR);

-- Tratamiento que requieren medicación por paciente, duración en días
SELECT '7. Tratamientos que requieren medicación por paciente, duración en días.' as ejercicio;

SELECT
	p.nombre as paciente,
	t.dosis,
	t.frecuencia,
	t.indicaciones,
	IFNULL(DATEDIFF(t.fecha_fin, t.fecha_inicio), 'ininterrumpido') as "duracion (días)"
FROM tratamientos  t
INNER JOIN pacientes p ON p.id_paciente = t.id_paciente
INNER JOIN catalogo_medicamentos cm ON t.id_medicamento = cm.id_medicamento
WHERE NOT ISNULL(t.id_medicamento);
