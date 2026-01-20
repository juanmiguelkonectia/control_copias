# Control de Copias de Impresora

Esta aplicación permite gestionar el **gasto de tóner** y registrar el uso de tu impresora de forma eficiente.

<img width="949" height="853" alt="image" src="https://github.com/user-attachments/assets/7920ba57-4e6b-4aec-b11e-e53904431923" />


### 📝 Características Principales

- **Control de consumibles:** Registra cambios de cartuchos y calcula su duración real.

- **Registro detallado:** Anota copias en blanco y negro o color con su fecha y propósito.

- **Visualización:** Genera gráficos de consumo para analizar tendencias de uso.

- **Exportación:** Permite extraer informes en formato **CSV**.

---

### 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python

- **Interfaz:** Tkinter

- **Base de Datos:** PostgreSQL (pgAdmin 4)

---

### 📂 Estructura del Proyecto

Plaintext

```
control_copias/
│
├── main.py      # Archivo principal
├── db.py        # Conexión base de datos
├── models.py    # Lógica de datos
└── config.py    # Configuración personal
```
- Ten en cuenta que en el archivo **config.py** has de añadir tu contraseña de pgAdmin 4 para que funcione
---

### 🚀 Instalación y Configuración

**1. Librerías necesarias:** Copia este comando en tu terminal: `pip install psycopg2` y `pip install matplotlib`, la primera permite a pyton conectarse con pgAdmin y la segunda nos permite dibujar la gráfica.

**2. Base de Datos SQL:** Crea la base de datos y las tablas necesarias con este código en pgAdmin:

SQL
```
CREATE DATABASE control_copias;
```

```
CREATE TABLE cartuchos (
    id SERIAL PRIMARY KEY,
    color CHAR(1) NOT NULL CHECK (color IN ('C','M','Y','K')),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activo BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE copias (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    copias_bn INTEGER NOT NULL DEFAULT 0,
    copias_color INTEGER NOT NULL DEFAULT 0,
    descripcion TEXT
);
```
### 🚀 Uso de la aplicación

<img width="853" height="768" alt="image" src="https://github.com/user-attachments/assets/8f6f0b91-abb4-4ab4-869b-ea1ebe2c1087" />

**1. Fecha de insertado:** Esta es la fecha en la que se colocó un nuevo toner de este color concreto.

**2. Fecha actual:** Esta es la fecha actual en que has abierto la aplicación por defecto la del cambio del toner, pero es modificable.

**3. Cambiar:** Aplicas la nueva fecha del cambio de toner. El contador de copias se pone a cero para él.

**4. Fecha actual:** Esta es la fecha actual en que has abierto la aplicación por defecto la de las copias que almacenes, pero es modificable.

**5. Número de copias en B/N:** Copias de blanco en negro que has realizado y quieres almacenar en tu base de datos.

**6. Número de copias en Color:** Copias de color que has realizado y quieres almacenar en tu base de datos.

**7. Descripción:** Por si quieres almacenar el objeto para el que se realizaron las copias.

**8. Guardar:** Almacena los datos en tu base de datos de SQL.

**9. Exportar CSV:** Exporta los datos de los tinteros en CSV.


