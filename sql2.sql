-- Partimos de un entorno limpio
DROP DATABASE IF EXISTS empresa_db;

-- Creamos la base de datos especificando de forma explicita el conjunto de caracteres y la collation
-- que en este caso son los mismos que los valores por defecto del server
CREATE DATABASE empresa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- Seleccionamos la base de datos
USE empresa_db;

-- Comprobamos que estamos en la base de datos
SELECT DATABASE();

-- Validamos que se ha creado con el caracter set y la collation
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'empresa_db';


-- Creación de tablas de la base de datos
SELECT '1. Crear, mediante instrucciones SQL, las tablas correspondientes al modelo relacional definido.' as ejercicio;

CREATE TABLE departamento (
    codDepto VARCHAR(4) PRIMARY KEY,
    nombreDpto VARCHAR(20) NOT NULL,
    Ciudad VARCHAR(15) NULL,
    codDirector VARCHAR(12) NULL
);

CREATE TABLE empleado (
    nDIEmp VARCHAR(12) PRIMARY KEY,
    nomEmp VARCHAR(30) NOT NULL,
    sexEmp CHAR(1) NOT NULL,
    fecNac DATE NOT NULL,
    fecIncorporacion DATE NOT NULL,
    salEmp DECIMAL(10, 2) NOT NULL,
    comisionE DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
    cargoE VARCHAR(20) NOT NULL,
    jefeID VARCHAR(12) NULL,
    codDepto VARCHAR(4) NOT NULL,

    FOREIGN KEY (jefeID) REFERENCES empleado(nDIEmp) ON DELETE SET NULL,
    FOREIGN KEY (codDepto) REFERENCES departamento(codDepto) ON DELETE RESTRICT
);

SELECT 'Tablas creadas correctamente' as resultado;


-- Generamos mock data para las tablas
SELECT '2. Insertar datos en cada una de las tablas: al menos 40 empleados y 10 departamentos.' as ejercicio;

INSERT INTO departamento (codDepto, nombreDpto, Ciudad, codDirector) VALUES
('1000', 'Direccion', 'Madrid', '10000000A'),
('2000', 'Ventas', 'Barcelona', '20000001B'),
('3000', 'Sistemas', 'Madrid', '20000002C'),
('4000', 'Recursos Humanos', 'Valencia', '20000003D'),
('5000', 'Marketing', 'Sevilla', '20000004E'),
('6000', 'Finanzas', 'Bilbao', '20000005F'),
('7000', 'Logistica', 'Zaragoza', '20000006G'),
('8000', 'Produccion', 'Malaga', '20000007H'),
('9000', 'Legal', 'Madrid', '20000008I'),
('9900', 'Investigacion', 'Valencia', '20000009J');

-- Nivel 1: Dirección General
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('10000000A', 'Carmen Torres', 'F', '1975-04-12', '2010-01-15', 95000.0, 0.0, 'Director Gral', NULL, '1000');

-- Nivel 2: Directores
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('20000001B', 'Luis Navarro', 'M', '1980-06-25', '2012-03-10', 65000.0, 5000.0, 'Dir. Ventas', '10000000A', '2000'),
('20000002C', 'Ana Romero', 'F', '1982-11-05', '2014-06-01', 62000.0, 0.0, 'Dir. Sistemas', '10000000A', '3000'),
('20000003D', 'Javier Gil', 'M', '1978-02-14', '2011-09-20', 60000.0, 0.0, 'Dir. RRHH', '10000000A', '4000'),
('20000004E', 'Elena Vidal', 'F', '1985-08-30', '2015-01-15', 58000.0, 2000.0, 'Dir. Marketing', '10000000A', '5000'),
('20000005F', 'Carlos Mora', 'M', '1979-12-10', '2013-05-12', 68000.0, 0.0, 'Dir. Finanzas', '10000000A', '6000'),
('20000006G', 'Marta Soler', 'F', '1983-07-22', '2016-11-01', 59000.0, 0.0, 'Dir. Logistica', '10000000A', '7000'),
('20000007H', 'David Costa', 'M', '1977-03-08', '2010-08-25', 61000.0, 0.0, 'Dir. Produccion','10000000A', '8000'),
('20000008I', 'Sara Reyes', 'F', '1986-09-15', '2018-02-10', 64000.0, 0.0, 'Dir. Legal', '10000000A', '9000'),
('20000009J', 'Pablo Leon', 'M', '1981-05-20', '2014-10-05', 66000.0, 0.0, 'Dir. I+D', '10000000A', '9900');

-- Nivel 3: Empleados
-- Dpto 2000 (Ventas)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('30000001K', 'Marcos Ruiz', 'M', '1990-01-10', '2019-02-01', 30000.0, 4000.0, 'Comercial', '20000001B', '2000'),
('30000002L', 'Lucia Vega', 'F', '1992-04-18', '2020-05-15', 29000.0, 4500.0, 'Comercial', '20000001B', '2000'),
('30000003M', 'Estrella Gil', 'F', '1988-11-22', '2018-08-10', 15000.0, 20000.0, 'Key Account', '20000001B', '2000'),
('30000004N', 'Sonia Rius', 'F', '1995-03-05', '2021-01-20', 28000.0, 3500.0, 'Comercial', '20000001B', '2000');

-- Dpto 3000 (Sistemas) -> Con algo de comisión para dar juego a la pregunta 9
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('30000005O', 'Ivan Cano', 'M', '1993-07-12', '2017-09-01', 40000.0, 1500.0, 'Programador', '20000002C', '3000'),
('30000006P', 'Laura Sanz', 'F', '1991-09-30', '2016-04-10', 42000.0, 2000.0, 'Analista', '20000002C', '3000'),
('30000007Q', 'Diego Mena', 'M', '1996-12-14', '2022-03-01', 35000.0, 500.0, 'Soporte TI', '20000002C', '3000'),
('30000008R', 'Clara Rico', 'F', '1989-02-25', '2015-11-20', 45000.0, 3000.0, 'DevOps', '20000002C', '3000');

-- Dpto 4000 (RRHH)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('30000009S', 'Ruben Diez', 'M', '1987-05-08', '2019-06-15', 36000.0, 0.0, 'Tecnico Selecc.', '20000003D', '4000'),
('30000010T', 'Paula Cruz', 'F', '1994-10-10', '2020-09-01', 34000.0, 0.0, 'Secretaria', '20000003D', '4000');

-- Dpto 5000 (Marketing)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('30000011U', 'Mario Vaca', 'M', '1992-08-14', '2018-04-12', 35000.0, 0.0, 'Diseñador', '20000004E', '5000'),
('30000012V', 'Ines Pino', 'F', '1990-12-05', '2017-07-22', 38000.0, 0.0, 'SEO Specialist','20000004E', '5000'),
('30000013W', 'Hugo Soto', 'M', '1995-02-18', '2021-08-01', 33000.0, 0.0, 'Copywriter', '20000004E', '5000');

-- Dpto 6000 (Finanzas)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('30000014X', 'Celia Muro', 'F', '1985-06-22', '2014-01-10', 42000.0, 0.0, 'Contable', '20000005F', '6000'),
('30000015Y', 'Tomas Rios', 'M', '1988-09-11', '2016-03-15', 40000.0, 0.0, 'Analista Finc.', '20000005F', '6000'),
('30000016Z', 'Nuria Alba', 'F', '1993-01-30', '2019-11-01', 36000.0, 0.0, 'Contable', '20000005F', '6000');

-- Dpto 7000 (Logistica)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('40000001A', 'Felix Pozo', 'M', '1982-04-15', '2015-05-20', 28000.0, 0.0, 'Coordinador', '20000006G', '7000'),
('40000002B', 'Rosa Luna', 'F', '1990-08-20', '2018-09-10', 25000.0, 0.0, 'Operario', '20000006G', '7000'),
('40000003C', 'Ivan Milla', 'M', '1994-11-25', '2021-02-15', 24000.0, 0.0, 'Operario', '20000006G', '7000');

-- Dpto 8000 (Produccion)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('40000004D', 'Luis Gago', 'M', '1980-12-10', '2012-07-01', 32000.0, 0.0, 'Jefe Turno', '20000007H', '8000'),
('40000005E', 'Eva Pardo', 'F', '1986-03-22', '2014-08-15', 26000.0, 0.0, 'Operario', '20000007H', '8000'),
('40000006F', 'Paco Coba', 'M', '1992-05-14', '2017-10-10', 26000.0, 0.0, 'Operario', '20000007H', '8000'),
('40000007G', 'Lola Royo', 'F', '1995-09-08', '2020-12-01', 25000.0, 0.0, 'Operario', '20000007H', '8000');

-- Dpto 9000 (Legal)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('40000008H', 'Juan Mora', 'M', '1984-07-30', '2016-01-20', 48000.0, 0.0, 'Abogado Junior', '20000008I', '9000'),
('40000012L', 'Elena Castro', 'F', '1988-10-15', '2017-04-10', 50000.0, 0.0, 'Abogado Senior', '20000008I', '9000'),
('40000013M', 'Marcos Rey', 'M', '1995-02-28', '2022-01-15', 30000.0, 0.0, 'Asesor Legal', '20000008I', '9000');

-- Dpto 9900 (Investigacion)
INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('40000009I', 'Alma Salas', 'F', '1990-02-12', '2018-06-10', 44000.0, 0.0, 'Investigador', '20000009J', '9900'),
('40000010J', 'Alex Duro', 'M', '1993-10-25', '2021-03-15', 41000.0, 0.0, 'Ingeniero I+D', '20000009J', '9900'),
('40000011K', 'Ruth Roig', 'F', '1996-06-18', '2022-09-01', 38000.0, 0.0, 'Ingeniero I+D', '20000009J', '9900'),
('40000014N', 'Victor Polo', 'M', '1989-11-05', '2015-05-20', 46000.0, 0.0, 'Cientifico Datos', '20000009J', '9900');

SELECT 'Datos insertados correctamente' as resultado;


-- Querys
SELECT '3. Obtener los datos de los empleados cuyo cargo sea ''Secretaria'' o ''Secretario''.' as ejercico;

SELECT * FROM empleado WHERE cargoE LIKE 'Secretari%';


SELECT '4. Obtener el nombre y la ciudad de los departamentos, ordenados por nombre en orden ascencete y ciudad en orden descendente.' as ejercicio;

SELECT nombreDpto, ciudad FROM departamento ORDER BY nombreDpto ASC, ciudad DESC;


SELECT '5. Obtener el nombre y el cargo de los empleados, ordenados por cargo y salario.' as ejercicio;

SELECT nomEmp as nombre, cargoE as cargo
FROM empleado ORDER BY salEmp DESC, cargoE;


SELECT '6. Obtener el nombre del departamento cuya suma total de salarios sea la más alta.' as ejercicio;

WITH salario_departamentos AS (
	SELECT codDepto, SUM(salEmp) as salario
	FROM empleado GROUP BY codDepto ORDER BY SUM(salEmp) DESC
	LIMIT 1
)

SELECT d.nombreDpto as departamento, s.salario
FROM salario_departamentos s
LEFT JOIN departamento d ON d.codDepto = s.codDepto;


SELECT '7. Obtener los salarios y las comisiones de los empleados del departamento 2000, ordenados por comisión.' as ejercicio;

SELECT
	nomEmp as empleado,
	salEmp as salario,
	comisionE as comision
FROM empleado
WHERE codDepto = '2000' ORDER BY comisionE DESC;


SELECT '8. Obtener todas las comisiones distintas, ordenadas por su valor.' as ejercicio;
-- no debería haber nulos en comisiones
SELECT DISTINCT comisionE FROM empleado ORDER BY comisionE DESC;

SELECT '9. Obtener, para cada empleado del departamento 3000, el valor total a pagar resultante de sumar una bonificación de 5.000 € a su salario, ordenado alfabéticamente por nombre del empleado.' as ejercicio;

SELECT
	nomEmp as empleado,
	salEmp as salario,
	comisionE as comision,
	salEmp + comisionE + 5000 as pago_total
FROM empleado
WHERE codDepto = '3000' ORDER BY nomEmp DESC;


SELECT '10. Obtener la lista de los empleados que ganan una comisión superior a su sueldo.' as ejercicio;

SELECT nomEmp as empleado FROM empleado WHERE comisionE > salEmp;


SELECT '11. Obtener los empleados cuya comisión es menor o igual que el 30% de su sueldo.' as ejercicio;

SELECT nomEmp as empleado FROM empleado WHERE comisionE <= (salEmp * 0.3);


SELECT '12. Obtener el documento de identidad, el nombre, el salario, la comisión y el salario total (salario + '
'comisión) de aquellos empleados cuya comisión sea superior a 10.000 €, ordenando el resultado por el '
'número de documento de identidad.' as ejercicio;

SELECT
	nDIEmp as documento,
	nomEmp as empleado,
	salEmp as salario,
	comisionE as comision,
	salEmp + comisionE as salario_total
FROM empleado
WHERE comisionE > 10000 ORDER BY nDIEmp;


SELECT '13. Obtener los datos de los empleados cuyo nombre comience por la letra ''M'', cuyo salario sea mayor de 40.000 o reciban comisión, y que trabajen en el departamento ''VENTAS''.' as ejercicio;

SELECT nomEmp as nombre FROM empleado
WHERE nomEmp LIKE 'M%'
	AND (salEmp > 40000 OR comisionE > 0)
	AND codDepto IN(
		SELECT codDepto FROM departamento WHERE UPPER(nombreDpto) = "VENTAS"
	);


SELECT '14. Obtener el nombre, el salario y la comisión de los empleados cuyo salario esté entre la mitad de la comisión y el valor de la propia comisión.' as ejercicio;

SELECT
	nomEmp as nombre,
	salEmp as salario,
	comisionE as comision
FROM empleado
WHERE salEmp BETWEEN comisionE/2 AND comisionE;


SELECT '15. Obtener el salario más alto, el más bajo y la diferencia entre ambos.' as ejercicio;

SELECT
	MAX(salEmp) as maximo,
	MIN(salEmp) as minimo,
	MAX(salEmp) - MIN(salEmp) as diff
FROM empleado;


SELECT '16. Obtener, por departamento, el número de empleados de sexo femenino y de sexo masculino.' as ejercicio;

WITH genero_por_departamento AS (
	SELECT
		codDepto,
		SUM(sexEmp = 'F') as sexo_femenino,
		SUM(sexEmp = 'M') as sexo_masculino
	FROM empleado
	GROUP BY codDepto
)

SELECT d.nombreDpto as departamento, g.sexo_femenino, g.sexo_masculino
FROM genero_por_departamento g
INNER JOIN departamento d ON d.codDepto = g.codDepto;


SELECT '17. Calcular el total de salarios por departamento.' as ejercicio;

SELECT d.nombreDpto as departamento, SUM(e.salEmp) as salario
FROM empleado e
LEFT JOIN departamento d ON d.codDepto = e.codDepto
GROUP BY d.nombreDpto ORDER BY SUM(e.salEmp) DESC ;


SELECT '18. Crear una vista que permita obtener la suma de salarios más alta entre todos los departamentos.' as ejercicio;

DROP VIEW IF EXISTS salario_maximo_departamento;

CREATE VIEW salario_maximo_departamento AS (
	SELECT d.nombreDpto, SUM(e.salEmp) as salario
	FROM empleado e
	LEFT JOIN departamento d ON d.codDepto = e.codDepto
	GROUP BY d.nombreDpto ORDER BY SUM(e.salEmp) DESC
	LIMIT 1
);

-- Check de la vista
SELECT TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'empresa_db';

SELECT * FROM salario_maximo_departamento;


SELECT '19. Crear un procedimiento almacenado que permita obtener los datos solicitados en la pregunta 13.' as ejercicio;
-- Ver: https://dev.mysql.com/doc/refman/9.7/en/create-procedure.html
DROP PROCEDURE IF EXISTS query_empleados;

delimiter //
CREATE PROCEDURE query_empleados (IN startsWith CHAR(1), IN departamento VARCHAR(20))
COMMENT "Filtra los empleado que cuyo nombre empieza por 'startsWith'
que cobren más de 40_000€ y que pertenezcan al departamento 'departamento'"
BEGIN
	SELECT nomEmp as nombre FROM empleado
	WHERE nomEmp LIKE CONCAT(startsWith, '%')
		AND (salEmp > 40000 OR comisionE > 0)
		AND codDepto IN(
			SELECT codDepto FROM departamento WHERE UPPER(nombreDpto) = UPPER(departamento)
		);
END//
delimiter ;

-- Check del procedure
SELECT ROUTINE_NAME, ROUTINE_TYPE, ROUTINE_DEFINITION, CREATED, ROUTINE_COMMENT FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'empresa_db';

CALL query_empleados('M', 'ventas');


SELECT '20. Crear un trigger que, cada vez que se inserte un nuevo empleado en la organización, registre '
'automáticamente dicha alta en una tabla de transacciones diarias. Crear también la tabla de '
'transacciones correspondiente (log de transacciones)' as ejercicio;

DROP TABLE IF EXISTS log_transacciones;

CREATE TABLE log_transacciones (
    id_transaccion INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fecha_evento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_evento VARCHAR(30),
    descripcion_evento VARCHAR(100)
);

DROP TRIGGER IF EXISTS update_log;

delimiter //
CREATE TRIGGER update_log AFTER INSERT ON empleado
FOR EACH ROW
	BEGIN
		INSERT INTO log_transacciones (tipo_evento, descripcion_evento) VALUES
		('Empleado nuevo', CONCAT(NEW.nomEmp, ' se ha incorporado al departamento ', NEW.codDepto));
	END//

delimiter ;

-- Check del trigger
SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_SCHEMA, EVENT_OBJECT_TABLE, ACTION_ORIENTATION, ACTION_TIMING  FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = 'empresa_db';

INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
('33303001L', 'Juanito Alimaña', 'M', '1989-01-10', '2025-02-01', 50000.0, 5000.0, 'Comercial', '20000001B', '2000');

SELECT * FROM log_transacciones;
