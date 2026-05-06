-- Activar soporte para foreign keys en sqlite (obligatorio por sesión)
-- Ver: https://sqlite.org/quirks.html#foreign_key_enforcement_is_off_by_default
-- Ver: https://sqlite.org/foreignkeys.html
PRAGMA foreign_keys = ON;

-- Creación de tablas de la base de datos
SELECT '1. Crear las tablas y sus relaciones.' as ejercicio;
-- Ver: https://sqlite.org/datatype3.html

CREATE TABLE pacientes (
    id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero TEXT CHECK(genero IN ('F', 'M', 'O')) NOT NULL,
    historial_medico TEXT,
    email TEXT UNIQUE,
    telefono TEXT,
    fecha_alta DATE NOT NULL
);

CREATE TABLE personal_medico (
    id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especialidad TEXT CHECK(especialidad IN ('Cirugia', 'Dermatologia', 'Enfermeria', 'Asistente', 'Otros')) NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT
);

CREATE TABLE catalogo_medicamentos (
    id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE facturas (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    fecha_factura DATETIME NOT NULL,
    concepto TEXT NOT NULL,
    monto NUMERIC NOT NULL,
    pagado BOOLEAN NOT NULL DEFAULT 0,
    detalle_transaccion TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT
);

CREATE TABLE citas (
    id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    id_factura INTEGER NOT NULL UNIQUE,
    fecha_cita DATETIME NOT NULL,
    motivo TEXT,
    confirmada BOOLEAN NOT NULL DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE RESTRICT
);

CREATE TABLE trasplantes (
    id_operacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_factura INTEGER NOT NULL UNIQUE,
    fecha_operacion DATETIME NOT NULL,
    tipo_procedimiento TEXT NOT NULL,
    zona_donante TEXT,
    zona_receptora TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE RESTRICT
);

CREATE TABLE equipo_operacion (
    id_operacion INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    rol TEXT CHECK(rol IN ('Responsable', 'Asistente')) NOT NULL,
    PRIMARY KEY (id_operacion, id_medico),
    FOREIGN KEY (id_operacion) REFERENCES trasplantes(id_operacion) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT
);

CREATE TABLE tratamientos (
    id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    id_factura INTEGER NULL,
    id_medicamento INTEGER NULL,
    dosis TEXT,
    frecuencia TEXT,
    indicaciones TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE SET NULL,
    FOREIGN KEY (id_medicamento) REFERENCES catalogo_medicamentos(id_medicamento) ON DELETE SET NULL
);

CREATE TABLE visitas_seguimiento (
    id_visita INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    fecha_visita DATETIME NOT NULL,
    observaciones TEXT,
    resultados TEXT,
    recomendaciones TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
    FOREIGN KEY (id_medico) REFERENCES personal_medico(id_medico) ON DELETE RESTRICT
);

CREATE TABLE documentacion (
    id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    tipo_documento TEXT NOT NULL,
    descripcion TEXT,
    ruta_archivo TEXT NOT NULL,
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
(1, 1, '2023-01-10 10:30:00', 'Consulta inicial de valoración', 100.00, 1, 'Pago con tarjeta'),
(2, 2, '2023-02-05 12:00:00', 'Consulta inicial de valoración', 100.00, 1, 'Pago con tarjeta'),
(3, 3, '2023-03-12 16:15:00', 'Consulta inicial de valoración', 100.00, 1, 'Pago en efectivo'),
(4, 1, '2023-04-20 09:00:00', 'Trasplante capilar FUE 2500 UFs', 4500.00, 1, 'Transferencia bancaria'),
(5, 2, '2023-06-15 11:45:00', 'Sesión de Plasma Rico en Plaquetas (PRP)', 250.00, 0, 'Pendiente de pago'),
(6, 4, '2023-04-01 10:30:00', 'Consulta inicial de valoración', 100.00, 1, 'Pago con tarjeta'),
(7, 5, '2023-05-15 11:00:00', 'Consulta por caída reaccional', 80.00, 1, 'Efectivo'),
(8, 3, '2023-06-10 08:30:00', 'Trasplante DHI 1500 UFs', 3200.00, 1, 'Financiado a 12 meses'),
(9, 4, '2023-04-15 10:00:00', 'Sesión de Mesoterapia Capilar', 150.00, 1, 'Tarjeta de crédito');

INSERT INTO citas (id_cita, id_paciente, id_medico, id_factura, fecha_cita, motivo, confirmada, observaciones) VALUES
(1, 1, 2, 1, '2023-01-10 10:00:00', 'Valoración de alopecia androgenética', 1, 'Paciente presenta patrón Norwood IV.'),
(2, 2, 2, 2, '2023-02-05 11:30:00', 'Consulta por caída de cabello postparto', 1, 'Efluvio telógeno, se recomienda tratamiento.'),
(3, 3, 1, 3, '2023-03-12 16:00:00', 'Segunda opinión sobre trasplante previo', 1, 'Se evalúan opciones para densificar coronilla.'),
(4, 4, 1, 6, '2023-04-01 10:00:00', 'Valoración para posible injerto', 1, 'Zona donante excelente. Apto para intervención.'),
(5, 5, 2, 7, '2023-05-15 10:30:00', 'Consulta por pérdida difusa', 1, 'Se manda analítica completa para descartar déficit de hierro.');

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

SELECT '4. Trasplantes identificando al paciente y al equipo médico.' as ejercicio;

SELECT
	m.nombre as medico,
	e.rol,
	p.nombre as paciente,
	t.fecha_operacion,
	t.zona_receptora,
	t.zona_donante
FROM trasplantes t
INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
INNER JOIN equipo_operacion e ON t.id_operacion = e.id_operacion
INNER JOIN personal_medico m ON e.id_medico = m.id_medico;

SELECT '5. Agrupando al equipo médico en un mismo registro.' as ejercicio;
-- group_concat no permite ordenar directamente en sqlite
-- Ver: https://sqlite.org/lang_aggfunc.html#group_concat

SELECT
    GROUP_CONCAT(personal_medico, ', ') AS equipo_medico,
    paciente,
    fecha_operacion,
    zona_receptora,
    zona_donante
FROM (
    SELECT
        m.nombre || ' [' || e.rol || ']' AS personal_medico,
        p.nombre AS paciente,
        t.fecha_operacion,
        t.zona_receptora,
        t.zona_donante
    FROM trasplantes t
    INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
    INNER JOIN equipo_operacion e ON t.id_operacion = e.id_operacion
    INNER JOIN personal_medico m ON e.id_medico = m.id_medico
    ORDER BY p.nombre, e.rol DESC, m.nombre
)
GROUP BY paciente, fecha_operacion, zona_receptora, zona_donante;

SELECT '6. Trazabilidad de las facturas que corresponder a trasplantes' as ejercicio;
-- sqlite no tiene un tipo de dato específico para fechas
-- Ver: https://sqlite.org/quirks.html#no_separate_datetime_datatype
-- Las funciones nos permiten operar con formatos de fecha y hora estándar ISO 8601 (YYYY-MM-DD HH:MM:SS)
-- Ver: https://sqlite.org/lang_datefunc.html

SELECT f.* FROM facturas f
WHERE EXISTS (SELECT * FROM trasplantes t
			  WHERE t.fecha_operacion BETWEEN datetime(f.fecha_factura, '-1 hour')
										  AND datetime(f.fecha_factura, '+1 hour'));

SELECT '7. Tratamientos que requieren medicación por paciente, duración en días.' as ejercicio;

SELECT
	p.nombre as paciente,
	t.dosis,
	t.frecuencia,
	t.indicaciones,
	COALESCE(julianday(t.fecha_fin) - julianday(t.fecha_inicio), 'ininterrumpido') as "duracion (días)"
FROM tratamientos  t
INNER JOIN pacientes p ON p.id_paciente = t.id_paciente
INNER JOIN catalogo_medicamentos cm ON t.id_medicamento = cm.id_medicamento
WHERE t.id_medicamento IS NOT NULL;
