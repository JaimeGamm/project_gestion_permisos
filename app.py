from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib

app = Flask(__name__)

# Clave secreta para sesiones Flask
app.secret_key = 'your_secret_key'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gamm1996'
app.config['MYSQL_DB'] = 'gestion_permisos_2db'

mysql = MySQL(app)


# Ruta de inicio de sesión de administradores y empleados
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()  # Encriptar el password

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id_usuario'] = account['id_usuario']
            session['nombre'] = account['nombre']
            session['rol'] = account['rol']  # Aquí agregamos el rol a la sesión

            flash('Inicio de sesión exitoso', 'success')

            # Redirigir según el rol
            if account['rol'] == 'administrador':
                return redirect(url_for('dashboard'))
            elif account['rol'] == 'empleado':
                return redirect(url_for('dashboard_empleado'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html')


# Ruta para el panel de control de administradores
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM permisos p JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.estado = "pendiente"')
        permisos = cursor.fetchall()
        return render_template('dashboard.html', permisos=permisos, nombre=session['nombre'])
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Ruta para ver el historial de permisos de un empleado
@app.route('/permisos/<int:id_usuario>')
def permisos(id_usuario):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, u.nombre AS empleado, a.nombre AS admin 
            FROM permisos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            LEFT JOIN usuarios a ON p.id_admin = a.id_usuario
            WHERE p.id_usuario = %s
        ''', (id_usuario,))
        permisos = cursor.fetchall()
        return render_template('permisos.html', permisos=permisos)
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id_usuario', None)
    session.pop('nombre', None)
    flash('Cerraste sesión exitosamente', 'success')
    return redirect(url_for('clear_flash'))


# Ruta para cambiar el estado de un permiso
@app.route('/cambiar_estado/<int:id_permiso>', methods=['POST'])
def cambiar_estado(id_permiso):
    if 'loggedin' in session and session['id_usuario']:  # Verifica que haya una sesión iniciada
        nuevo_estado = request.form['estado']
        comentario_admin = request.form.get('comentario', '')  # Obtener comentario si existe
        id_admin = session['id_usuario']  # El administrador que cambia el estado

        cursor = mysql.connection.cursor()
        # Actualizar el estado del permiso, registrar el administrador y el comentario
        cursor.execute('''
            UPDATE permisos 
            SET estado = %s, id_admin = %s, comentarios_admin = %s, fecha_revision = NOW()
            WHERE id_permiso = %s
        ''', (nuevo_estado, id_admin, comentario_admin, id_permiso))
        mysql.connection.commit()

        flash(f'El permiso ha sido {nuevo_estado}', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Ruta para ver todos los permisos
@app.route('/todos_los_permisos')
def todos_los_permisos():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT p.*, u.nombre AS empleado, a.nombre AS admin FROM permisos p LEFT JOIN usuarios u ON p.id_usuario = u.id_usuario LEFT JOIN usuarios a ON p.id_admin = a.id_usuario')
        permisos = cursor.fetchall()
        return render_template('todos_permisos.html', permisos=permisos)
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Ruta para registrar un nuevo usuario
@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if 'loggedin' in session and session['rol'] == 'administrador':
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            password = hashlib.md5(request.form['password'].encode()).hexdigest()  # Encriptar la contraseña
            rol = request.form['rol']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)', (nombre, email, password, rol))
            mysql.connection.commit()

            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('registrar_usuario.html')
    else:
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('login'))

@app.route('/dashboard_empleado')
def dashboard_empleado():
    if 'loggedin' in session and session['rol'] == 'empleado':
        id_usuario = session['id_usuario']

        # Obtener el historial de permisos del empleado
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM permisos WHERE id_usuario = %s', (id_usuario,))
        permisos = cursor.fetchall()

        return render_template('dashboard_empleado.html', permisos=permisos, nombre=session['nombre'])
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Ruta para solicitar un permiso
@app.route('/solicitar_permiso', methods=['GET', 'POST'])
def solicitar_permiso():
    if 'loggedin' in session and session['rol'] == 'empleado':
        if request.method == 'POST':
            id_usuario = session['id_usuario']
            tipo_permiso = request.form['tipo_permiso']
            descripcion = request.form['descripcion']
            fecha_permiso = request.form['fecha_permiso']
            hora_inicio = request.form['hora_inicio']
            hora_fin = request.form['hora_fin']

            cursor = mysql.connection.cursor()
            
            # Insertar la solicitud de permiso
            cursor.execute('''
                INSERT INTO permisos (id_usuario, tipo_permiso, descripcion, fecha_permiso, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (id_usuario, tipo_permiso, descripcion, fecha_permiso, hora_inicio, hora_fin))
            mysql.connection.commit()

            # Obtener el ID del permiso recién insertado
            id_permiso = cursor.lastrowid

            # Verificar y modificar el estado del permiso automáticamente
            nuevo_estado, comentario_admin = verificar_permiso_automatico(id_usuario, tipo_permiso, fecha_permiso, hora_inicio, hora_fin)

            # Actualizar el estado del permiso si ha cambiado
            if nuevo_estado:
                cursor.execute('''
                    UPDATE permisos SET estado = %s, comentarios_admin = %s
                    WHERE id_permiso = %s
                ''', (nuevo_estado, comentario_admin, id_permiso))
                mysql.connection.commit()

            flash('Permiso solicitado exitosamente', 'success')
            return redirect(url_for('dashboard_empleado'))

        return render_template('solicitar_permiso.html')
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Función para verificar reglas automáticas de permisos
def verificar_permiso_automatico(id_usuario, tipo_permiso, fecha_permiso, hora_inicio, hora_fin):
    cursor = mysql.connection.cursor()

    # Regla 1: Rechazar permisos de salud si el empleado ha solicitado más de 3 en el mismo mes
    if tipo_permiso == 'salud':
        cursor.execute('''
            SELECT COUNT(*) FROM permisos
            WHERE id_usuario = %s AND tipo_permiso = 'salud'
            AND MONTH(fecha_permiso) = MONTH(%s)
            AND YEAR(fecha_permiso) = YEAR(%s)
        ''', (id_usuario, fecha_permiso, fecha_permiso))
        conteo_permisos = cursor.fetchone()[0]
        if conteo_permisos >= 3:
            comentario_admin = 'Rechazado automáticamente: Se ha solicitado más de 3 permisos de salud este mes (Regla 1).'
            return 'rechazado', comentario_admin

    # Regla 2: Aprobar automáticamente si no ha habido permisos en los últimos 60 días
    cursor.execute('''
        SELECT COUNT(*) FROM permisos
        WHERE id_usuario = %s AND fecha_permiso >= DATE_SUB(%s, INTERVAL 60 DAY)
    ''', (id_usuario, fecha_permiso))
    permisos_ultimos_60_dias = cursor.fetchone()[0]
    if permisos_ultimos_60_dias == 0:
        comentario_admin = 'Aprobado automáticamente: No ha habido permisos en los últimos 60 días (Regla 2).'
        return 'aprobado', comentario_admin

    # Regla 3: Cancelar si se solapan con otro permiso ya aprobado
    cursor.execute('''
        SELECT COUNT(*) FROM permisos
        WHERE id_usuario = %s AND fecha_permiso = %s
        AND hora_inicio < %s AND hora_fin > %s
        AND estado = 'aprobado'
    ''', (id_usuario, fecha_permiso, hora_fin, hora_inicio))
    permisos_solapados = cursor.fetchone()[0]
    if permisos_solapados > 0:
        comentario_admin = 'Cancelado automáticamente: El permiso se solapa con otro permiso aprobado (Regla 3).'
        return 'cancelado', comentario_admin

    # Si no se aplica ninguna regla, dejar el estado como pendiente
    return None, None


@app.route('/clear_flash')
def clear_flash():
    session.pop('_flashes', None)
    return redirect(url_for('login'))

@app.route('/top_empleados')
def top_empleados():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Consulta SQL para obtener el top 5 de empleados con más permisos solicitados este mes
        cursor.execute('''
            SELECT u.nombre, COUNT(p.id_permiso) AS total_permisos
            FROM permisos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE MONTH(p.fecha_solicitud) = MONTH(CURRENT_DATE)
            GROUP BY u.nombre
            ORDER BY total_permisos DESC
            LIMIT 5
        ''')
        top_empleados = cursor.fetchall()
        return {"top_empleados": top_empleados}
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))

# Ruta para obtener el número de permisos solicitados por mes en el año
@app.route('/permisos_por_mes')
def permisos_por_mes():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Consulta SQL para obtener el número de permisos solicitados por mes en el año actual
        cursor.execute('''
            SELECT MONTH(fecha_permiso) AS mes, COUNT(id_permiso) AS total_permisos
            FROM permisos
            WHERE YEAR(fecha_permiso) = YEAR(CURRENT_DATE)
            GROUP BY mes
            ORDER BY mes;
        ''')
        permisos_por_mes = cursor.fetchall()
        return {"permisos_por_mes": permisos_por_mes}
    else:
        flash('Por favor inicia sesión', 'danger')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
