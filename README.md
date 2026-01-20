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

---

### 🚀 Instalación y Configuración

**1. Librerías necesarias:** Copia este comando en tu terminal: `pip install psycopg2 matplotlib`

**2. Base de Datos SQL:** Crea las tablas con este código en pgAdmin:

SQL

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

luego
