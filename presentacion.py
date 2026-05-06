import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Modelado de datos
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    database_dir = mo.notebook_location() / "public"
    return (database_dir,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | Info
        type: info

    Para poder ejecutar este cuaderno de forma interactiva las bases de datos de han replicado en **sqlite3**.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Primera parte: Diseño de base de datos para clínica capilar
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Consideraciones iniciales
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    El diseño de la base de datos se va a realizar teniendo en cuenta, las tablas y atributos propuestos como parte del enunciado del ejercicio y las siguientes consideraciones:

    - Para ser registrado como **paciente**, es indispensable tener al menos una cita agendada, lo cual implica la generación de al menos una factura.
    - Los **trasplantes** son supervisados por un **equipo médico** que puede estar compuesto por varios miembros (roles definidos).
    - Las **citas** y las **visitas de seguimiento** son atendidas por un único miembro del **equipo médico**.
    - Cada **tratamiento** es único y específico de un cliente.
    - Los **tratamientos** no requieren la obligatoriedad de administrar un medicamento. Los **medicamentos** recetados en los tratamientos se normalizan en una tabla independiente `CATALOGO_MEDICAMENTOS`.
    - Las **visitas de seguimiento** y los **tratamientos** se almacenan como hechos clínicos independientes para mayor flexibilidad.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Diagrama Entity Relationship
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    El siguiente diagrama se puede visualizar de forma interactiva en el repositorios de github, donde se aloja el código de este proyecto y en mi perfil de mermaid:

    - [Enlace al repositorio.](https://github.com/adecora/clinica-capilar)
    - [Enlace al diagrama en mermaid.](https://mermaid.ai/app/projects/8363ba3c-d1ca-48a7-9c12-52bbb2cf2a32/diagrams/fbf173ba-1709-442f-9644-ea6a0cad80fc/version/v0.1/edit)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid("""
    ---
    title: Base de datos para la gestión de trasplantes capilares
    ---
    erDiagram
      %% Definición de entidades
      PACIENTES {
        INT id_paciente PK "NOT NULL AUTO_INCREMENT"
        VARCHAR nombre "NOT NULL"
        DATE fecha_nacimiento "NOT NULL"
        ENUM genero  "('F', 'M', 'O') NOT NULL"
        TEXT historial_medico
        VARCHAR email "UNIQUE"
        VARCHAR telefono
        DATE fecha_alta "NOT NULL"
      }

      PERSONAL_MEDICO {
        INT id_medico PK "NOT NULL AUTO_INCREMENT"
        VARCHAR nombre "NOT NULL"
        ENUM especialidad "('Cirugia', 'Dermatologia', 'Enfermeria', 'Asistente', 'Otros') NOT NULL"
        VARCHAR email "UNIQUE"
        VARCHAR telefono
      }

      EQUIPO_OPERACION {
        INT id_operacion PK, FK
        INT id_medico PK, FK
        ENUM rol "('Responsable', 'Asistente') NOT NULL"
      }

      TRASPLANTES {
        INT id_operacion PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        INT id_factura FK "NOT NULL"
        DATETIME fecha_operacion "NOT NULL"
        VARCHAR tipo_procedimiento "NOT NULL"
        VARCHAR zona_donante
        VARCHAR zona_receptora
      }

      CITAS {
        INT id_cita PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        INT id_medico FK "NOT NULL"
        INT id_factura FK "NOT NULL"
        DATETIME fecha_cita "NOT NULL"
        VARCHAR motivo
        BOOL confirmada "NOT NULL DEFAULT FALSE"
        TEXT observaciones
      }

      VISITAS_SEGUIMIENTO {
        INT id_visita PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        INT id_medico FK "NOT NULL"
        DATETIME fecha_visita "NOT NULL"
        TEXT observaciones
        VARCHAR resultados
        VARCHAR recomendaciones
      }

      TRATAMIENTOS {
        INT id_tratamiento PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        INT id_medico FK "NOT NULL"
        INT id_factura FK  "NULL"
        INT id_medicamento FK "NULL"
        VARCHAR dosis
        VARCHAR frecuencia
        VARCHAR indicaciones
        DATE fecha_inicio "NOT NULL"
        DATE fecha_fin
      }

      CATALOGO_MEDICAMENTOS {
        INT id_medicamento PK "NOT NULL AUTO_INCREMENT"
        VARCHAR nombre
      }

      DOCUMENTACION {
        INT id_documento PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        VARCHAR tipo_documento "NOT NULL"
        VARCHAR descripcion
        VARCHAR ruta_archivo "NOT NULL"
        DATE fecha_documento
      }

      FACTURAS {
        INT id_factura PK  "NOT NULL AUTO_INCREMENT"
        INT id_paciente FK "NOT NULL"
        DATETIME fecha_factura "NOT NULL"
        VARCHAR concepto "NOT NULL"
        DECIMAL monto "NOT NULL"
        BOOL pagado "NOT NULL DEFAULT FALSE"
        VARCHAR detalle_transaccion
      }


      %% Defición de relaciones
      PACIENTES ||--|{ CITAS : "agenda"
      PACIENTES ||--|{ FACTURAS : "es titular de"
      PACIENTES ||--o{ DOCUMENTACION : "posee"
      PACIENTES ||--o{ TRASPLANTES : "se somete a"
      PACIENTES ||--o{ TRATAMIENTOS : "recibe"
      PACIENTES ||--o{ VISITAS_SEGUIMIENTO : "realiza"

      PERSONAL_MEDICO ||--o{ CITAS : "atiende"
      PERSONAL_MEDICO ||--o{ EQUIPO_OPERACION : "participa en"
      PERSONAL_MEDICO ||--o{ TRATAMIENTOS : "prescribe"
      PERSONAL_MEDICO ||--o{ VISITAS_SEGUIMIENTO : "atiende"

      TRASPLANTES ||--|{ EQUIPO_OPERACION : "requiere"

      FACTURAS ||--|{ CITAS : "cobra"
      FACTURAS ||--|{ TRASPLANTES : "cobra"
      FACTURAS ||--o{ TRATAMIENTOS : "cobra"

      CATALOGO_MEDICAMENTOS ||--o{ TRATAMIENTOS : "incluido en"


      %% Estilos
      %% Grupo 1: Core / Paciente (Azul)
      classDef core fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      class PACIENTES,DOCUMENTACION core

      %% Grupo 2: Equipo Médico (Verde)
      classDef medical fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
      class PERSONAL_MEDICO,EQUIPO_OPERACION medical

      %% Grupo 3: Eventos Clínicos y Acciones (Naranja)
      classDef events fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
      class CITAS,TRASPLANTES,VISITAS_SEGUIMIENTO,TRATAMIENTOS events

      %% Grupo 4: Catálogos y Admin/Facturación (Morado/Gris)
      classDef admin fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
      class FACTURAS admin

      classDef catalog fill:#eceff1,stroke:#455a64,stroke-width:2px
      class CATALOGO_MEDICAMENTOS catalog
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Decisiones de diseño y tipos de datos
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Detalle de los tipos escogidos para los atributos de la base de datos:

    - Tipos numéricos:
      * **INT:** Usados con *auto-increment y NOT NULL* como claves primarias de las tablas. Ver: [documentación.](https://dev.mysql.com/doc/refman/8.4/en/primary-key-optimization.html)
      * [**DECIMAL:**](https://dev.mysql.com/doc/refman/8.4/en/fixed-point-types.html) Para obtener precisión numérica al trabajar con *facturas*.
      * [**BOOL:**](https://dev.mysql.com/doc/refman/8.4/en/numeric-type-syntax.html) Cuando solo requerimos almacenar `TRUE`o `FALSE`, en el caso de la *confirmación de citas y el pago de facturas.*
    - Tipos fecha:
      * **DATE:** Cuando no necesitamos precisión de `hh:mm:ss`.
      * **DATETIME:** Cuando requerimos `hh:mm:ss` en el caso de *trasplantes, citas, visitas y facturas*. Se usa sin fracciones de segundo, [comportamiento por defecto.](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-type-syntax.html)
    - Tipos cadena de texto:
      * **VARCHAR:** Para campos de tamaño mediano.
      * [**TEXT:**](https://dev.mysql.com/doc/refman/8.4/en/blob.html) En el caso de las *observaciones de citas y visitas de seguimiento e historial médico* requerimos mayor flexibilidad.
      * [**ENUM:**](https://dev.mysql.com/doc/refman/8.4/en/enum.html) Para los casos donde la lista de valores es predefinida, optimizan el almacenamiento guardando las opciones como números.

    - Para las **foreing keys** usaremos **RESTRICT** para los casos más restrictivos, p.ej. no podemos borrar un paciente si tiene facturas, trasplantes o tratamiento por ejemplo.

    El código completo del ejercicio resuelto se encuentra en [**sql1.sql**](https://github.com/adecora/clinica-capilar/blob/master/sql1.sql).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Crear las tablas y sus relaciones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
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
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Insertar datos en cada una de las tablas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
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
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. SELECT de los datos de cada tabla.
    """)
    return


@app.cell
def _(database_dir):
    import sqlalchemy
    from pathlib import Path

    _db_source = database_dir / "clinica_capilar.db"

    if str(_db_source).startswith("http"):
        import urllib.request

        _local_db = Path("/tmp/clinica_capilar.db")
        urllib.request.urlretrieve(str(_db_source), _local_db)

        _DATABASE_URL = "sqlite:///" + str(_local_db)
    else:
        _DATABASE_URL = "sqlite:///" + str(_db_source)

    clinica_capilar = sqlalchemy.create_engine(_DATABASE_URL)
    return Path, clinica_capilar, sqlalchemy, urllib


@app.cell
def _(clinica_capilar, mo):
    _df = mo.sql(
        f"""
        -- Activar soporte para foreign keys en sqlite (obligatorio por sesión)
        -- Ver: https://sqlite.org/quirks.html#foreign_key_enforcement_is_off_by_default
        -- Ver: https://sqlite.org/foreignkeys.html
        PRAGMA foreign_keys = ON;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, mo, pacientes):
    _df = mo.sql(
        f"""
        SELECT * FROM pacientes;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, mo, personal_medico):
    _df = mo.sql(
        f"""
        SELECT * FROM personal_medico;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(catalogo_medicamentos, clinica_capilar, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM catalogo_medicamentos;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, facturas, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM facturas;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(citas, clinica_capilar, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM citas;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, mo, trasplantes):
    _df = mo.sql(
        f"""
        SELECT * FROM trasplantes;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, equipo_operacion, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM equipo_operacion;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, mo, tratamientos):
    _df = mo.sql(
        f"""
        SELECT * FROM tratamientos;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, mo, visitas_seguimiento):
    _df = mo.sql(
        f"""
        SELECT * FROM visitas_seguimiento;
        """,
        engine=clinica_capilar
    )
    return


@app.cell
def _(clinica_capilar, documentacion, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM documentacion;
        """,
        engine=clinica_capilar
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. Trasplantes identificando al paciente y al equipo médico.
    """)
    return


@app.cell
def _(
    clinica_capilar,
    equipo_operacion,
    mo,
    pacientes,
    personal_medico,
    trasplantes,
):
    _df = mo.sql(
        f"""
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
        """,
        engine=clinica_capilar
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Agrupando al equipo médico en un mismo registro.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | En mysql

    `GROUP_CONCAT` acepta direactamente los parámetros de ordenación.

    ```sql
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
    ```

    ///
    """)
    return


@app.cell
def _(
    clinica_capilar,
    equipo_operacion,
    mo,
    pacientes,
    personal_medico,
    trasplantes,
):
    _df = mo.sql(
        f"""
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
        """,
        engine=clinica_capilar
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. Trazabilidad de las facturas que corresponder a trasplantes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | En mysql

    Podemos trabajar direactamente con las fechas.

    ```sql
    SELECT f.* FROM facturas f
    WHERE EXISTS (SELECT * FROM trasplantes t
    			  WHERE t.fecha_operacion BETWEEN f.fecha_factura - INTERVAL 1 HOUR
    										  AND f.fecha_factura + INTERVAL 1 HOUR);
    ```

    ///
    """)
    return


@app.cell
def _(clinica_capilar, facturas, mo, trasplantes):
    _df = mo.sql(
        f"""
        SELECT f.* FROM facturas f
        WHERE EXISTS (SELECT * FROM trasplantes t
        			  WHERE t.fecha_operacion BETWEEN datetime(f.fecha_factura, '-1 hour')
        										  AND datetime(f.fecha_factura, '+1 hour'));
        """,
        engine=clinica_capilar
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Tratamientos que requieren medicación por paciente, duración en días.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | En mysql

    ```sql
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
    ```

    ///
    """)
    return


@app.cell
def _(catalogo_medicamentos, clinica_capilar, mo, pacientes, tratamientos):
    _df = mo.sql(
        f"""
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
        """,
        engine=clinica_capilar
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Segunda parte: Implementación y consultas sobre modelo relacional dado
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Desarrollo de una base de datos a partir de un modelo relacional dado.

    El ćodigo completo del ejercicio resuelto se encuentra en [**sql2.sql**](https://github.com/adecora/clinica-capilar/blob/master/sql2.sql).
    """)
    return


@app.cell
def _(Path, database_dir, sqlalchemy, urllib):
    _db_source = database_dir / "empresa.db"

    if str(_db_source).startswith("http"):
        _local_db = Path("/tmp/empresa.db")
        urllib.request.urlretrieve(str(_db_source), _local_db)

        _DATABASE_URL = "sqlite:///" + str(_local_db)
    else:
        _DATABASE_URL = "sqlite:///" + str(_db_source)

    empresa = sqlalchemy.create_engine(_DATABASE_URL)
    return (empresa,)


@app.cell
def _(empresa, mo):
    _df = mo.sql(
        f"""
        PRAGMA foreign_keys = ON;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **1.** Crear, mediante instrucciones SQL, las tablas correspondientes al modelo relacional definido.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
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
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Validamos que el modelo relacional creado es igual al modelo relacional de dado en el ejemplo.

    ![Modelo relacional generado con mysql reverse tool](public/modelo-relacional.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **2.** Insertar datos en cada una de las tablas: al menos 40 empleados y 10 departamentos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```sql
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
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **3.** Obtener los datos de los empleados cuyo cargo sea 'Secretario' o 'Secreteria'
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM empleado WHERE cargoE LIKE 'Secretari%';
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### **4.** Obtener el nombre y la ciudad de los departamentos, ordenados por nombre en orden ascendente ciudad en orden descedente
    """)
    return


@app.cell
def _(departamento, empresa, mo):
    sol = mo.sql(
        f"""
        SELECT nombreDpto, ciudad FROM departamento ORDER BY nombreDpto ASC, ciudad DESC;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **5.** Obtener el nombre y el cargo de los empleados, ordenados por cargo y salario.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as nombre, cargoE as cargo
        FROM empleado ORDER BY salEmp DESC, cargoE;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **6.**  Obtener el nombre del departamento cuya suma total de salarios sea la más alta.
    """)
    return


@app.cell
def _(departamento, empleado, empresa, mo):
    _df = mo.sql(
        f"""
        WITH salario_departamentos AS (
        	SELECT codDepto, SUM(salEmp) as salario
        	FROM empleado GROUP BY codDepto ORDER BY SUM(salEmp) DESC
        	LIMIT 1
        )
        SELECT d.nombreDpto as departamento, s.salario
        FROM salario_departamentos s
        LEFT JOIN departamento d ON d.codDepto = s.codDepto;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **7.** Obtener los salarios y las comisiones de los empleados del departamento 2000, ordenados por comisión.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as empleado, salEmp as salario, comisionE as comision
        FROM empleado WHERE codDepto = '2000' ORDER BY comisionE DESC;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **8.** Obtener todas las comisiones distintas, ordenadas por su valor.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT comisionE FROM empleado ORDER BY comisionE DESC;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **9.** Obtener, para cada empleado del departamento 3000, el valor total a pagar resultante de sumar una bonificación de 5.000 € a su salario, ordenado alfabéticamente por nombre del empleado.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as empleado, salEmp as salario, comisionE as comision, salEmp + comisionE + 5000 as pago_total
        FROM empleado WHERE codDepto = '3000' ORDER BY nomEmp DESC;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **10.** Obtener la lista de los empleados que ganan una comisión superior a su sueldo.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as empleado FROM empleado WHERE comisionE > salEmp;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **11.** Obtener los empleados cuya comisión es menor o igual que el 30% de su sueldo.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as empleado FROM empleado WHERE comisionE <= (salEmp * 0.3);
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **12.** Obtener el documento de identidad, el nombre, el salario, la comisión y el salario total (salario + comisión) de aquellos empleados cuya comisión sea superior a 10.000 €, ordenando el resultado por el número de documento de identidad.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nDIEmp as documento, nomEmp as empleado, salEmp as salario, comisionE as comision, salEmp + comisionE as salario_total
        FROM empleado WHERE comisionE > 10000 ORDER BY nDIEmp;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **13.** Obtener los datos de los empleados cuyo nombre comience por la letra 'M', cuyo salario sea mayor de 40.000 o reciban comisión, y que trabajen en el departamento 'VENTAS'.
    """)
    return


@app.cell
def _(departamento, empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as nombre FROM empleado
        WHERE nomEmp LIKE 'M%'
        	AND (salEmp > 40000 OR comisionE > 0)
        	AND codDepto IN(
        		SELECT codDepto FROM departamento WHERE UPPER(nombreDpto) = 'VENTAS'
        	);
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **14.** Obtener el nombre, el salario y la comisión de los empleados cuyo salario esté entre la mitad de la comisión y el valor de la propia comisión.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT nomEmp as nombre, salEmp as salario, comisionE as comision
        FROM empleado WHERE salEmp BETWEEN comisionE/2 AND comisionE;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **15.** Obtener el salario más alto, el más bajo y la diferencia entre ambos.
    """)
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT MAX(salEmp) as maximo, MIN(salEmp) as minimo, MAX(salEmp) - MIN(salEmp) as diff FROM empleado;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **16.** Obtener, por departamento, el número de empleados de sexo femenino y de sexo masculino.
    """)
    return


@app.cell
def _(departamento, empleado, empresa, mo):
    _df = mo.sql(
        f"""
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
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **17.** Calcular el total de salarios por departamento.
    """)
    return


@app.cell
def _(departamento, empleado, empresa, mo):
    _df = mo.sql(
        f"""
        SELECT d.nombreDpto as departamento, SUM(e.salEmp) as salario
        FROM empleado e
        LEFT JOIN departamento d ON d.codDepto = e.codDepto
        GROUP BY d.nombreDpto ORDER BY SUM(e.salEmp) DESC ;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **18.** Crear una vista que permita obtener la suma de salarios más alta entre todos los departamentos.
    """)
    return


@app.cell
def _(departamento, empleado, empresa, mo):
    _df = mo.sql(
        f"""
        CREATE VIEW IF NOT EXISTS salario_maximo_departamento AS
        	SELECT d.nombreDpto, SUM(e.salEmp) as salario
        	FROM empleado e
        	LEFT JOIN departamento d ON d.codDepto = e.codDepto
        	GROUP BY d.nombreDpto ORDER BY SUM(e.salEmp) DESC
        	LIMIT 1;
        """,
        engine=empresa
    )
    return


@app.cell
def _(empresa, mo, sqlite_master):
    _df = mo.sql(
        f"""
        SELECT * FROM sqlite_master WHERE type='view';
        """,
        engine=empresa
    )
    return


@app.cell
def _(empresa, mo, salario_maximo_departamento):
    _df = mo.sql(
        f"""
        SELECT * FROM salario_maximo_departamento;
        """,
        engine=empresa
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **19.** Crear un procedimiento almacenado que permita obtener los datos solicitados en la pregunta 13.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | **OJO!!!**
        type: danger

    En sqlite no se pueden crear procedures (procedimientos almacenados), el código en mysql es:

    ```sql
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
    ```
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **20.** Crear un trigger que, cada vez que se inserte un nuevo empleado en la organización, registre automáticamente dicha alta en una tabla de transacciones diarias. Crear también la tabla de transacciones correspondiente (log de transacciones).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | En mysql

    ```sql
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
    ```

    ///
    """)
    return


@app.cell
def _(empresa, mo):
    _df = mo.sql(
        f"""
        CREATE TABLE IF NOT EXISTS log_transacciones (
            id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_evento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tipo_evento TEXT,
            descripcion_evento TEXT
        );
        """,
        engine=empresa
    )
    return


@app.cell
def _(empresa, mo):
    _df = mo.sql(
        f"""
        CREATE TRIGGER IF NOT EXISTS update_log AFTER INSERT ON empleado
        BEGIN
            INSERT INTO log_transacciones (tipo_evento, descripcion_evento) VALUES
            ('Empleado nuevo', NEW.nomEmp || ' se ha incorporado al departamento ' || NEW.codDepto);
        END;
        """,
        engine=empresa
    )
    return


@app.cell
def _(empresa, mo, sqlite_master):
    _df = mo.sql(
        f"""
        SELECT * FROM sqlite_master WHERE type='trigger';
        """,
        engine=empresa
    )
    return


@app.cell
def _(empleado, empresa, mo):
    _df = mo.sql(
        f"""
        INSERT INTO empleado (nDIEmp, nomEmp, sexEmp, fecNac, fecIncorporacion, salEmp, comisionE, cargoE, jefeID, codDepto) VALUES
        ('33303001L', 'Juanito Alimaña', 'M', '1989-01-10', '2025-02-01', 50000.0, 5000.0, 'Comercial', '20000001B', '2000');
        """,
        engine=empresa
    )
    return


@app.cell
def _(empresa, log_transacciones, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM log_transacciones;
        """,
        engine=empresa
    )
    return


if __name__ == "__main__":
    app.run()
