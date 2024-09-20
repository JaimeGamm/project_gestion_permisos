# Gestión de Permisos - Flask App

Este es un proyecto de gestión de permisos para empleados desarrollado en Flask con MySQL como base de datos. Los empleados pueden solicitar permisos, y los administradores pueden aprobar o rechazar estos permisos.

## Requisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.x** (preferiblemente la última versión)
- **MySQL** (con un usuario y base de datos configurados)
- **Flask** y otros paquetes necesarios

## Instalación

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/usuario/project_gestion_permisos.git
    cd project_gestion_permisos
    ```

2. Crea un entorno virtual (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate   # En Linux/macOS
    venv\Scripts\activate      # En Windows
    ```

3. Instala Flask y Flask-MySQLdb:

    ```bash
    pip install Flask Flask-MySQLdb
    ```

4. Instala las demás dependencias utilizando el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración de la Base de Datos

1. **Asegúrate de tener MySQL instalado y en funcionamiento**. Si no lo tienes instalado, puedes descargarlo desde [aquí](https://dev.mysql.com/downloads/installer/).

2. Crea la base de datos en MySQL utilizando el siguiente comando:

    ```sql
    CREATE DATABASE gestion_permisos_2db;
    ```

3. Ahora, ejecuta el script SQL para crear las tablas necesarias. El archivo `project_gestion_permisos_sql.sql` contiene las tablas y relaciones necesarias. Puedes ejecutarlo en MySQL de la siguiente manera:

    ```bash
    mysql -u tu_usuario -p gestion_permisos_2db < project_gestion_permisos_sql.sql
    ```

4. **Configuración del administrador**: Si deseas crear un administrador para el sistema, puedes ejecutar el script `admin_script.py` que generará un usuario administrador en la base de datos:

    ```bash
    python admin_script.py
    ```

## Configuración de Flask

Asegúrate de configurar las credenciales de acceso a MySQL en el archivo de configuración de Flask. En el archivo `app.py`, puedes configurar la base de datos como sigue:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'gestion_permisos_2db'
