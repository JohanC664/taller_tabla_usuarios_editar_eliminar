from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2',
}

# mysql connection configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskusuarios'
mysql = MySQL(app)

# --------------------------------------------------#
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    return render_template('index.html', usuarioos=data)

# --------------------------------------------------#
@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        apellido_usuario = request.form['apellido_usuario']
        email_usuario = request.form['email_usuario']
        direccion_usuario = request.form['direccion_usuario']
        telefono_usuario = request.form['telefono_usuario']
        usuario_usuario = request.form['usuario_usuario']
        contrasena_usuario = request.form['contrasena_usuario']
        roles = request.form.get('txtrol')

        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM personas WHERE emailper = %s OR usuarioper = %s', (email_usuario, usuario_usuario))
        existe = cur.fetchall()

        if existe:
            for v in existe:
                if v[3] == email_usuario and v[6] == usuario_usuario:
                    flash("El email y el usuario ya existen.", "mensaje")
                elif v[3] == email_usuario:
                    flash("El email ya existe.", "me")
                elif v[6] == usuario_usuario:
                    flash("El usuario ya existe.", "mu")
            return redirect(url_for("index"))
        else:
            cur.execute("INSERT INTO personas(nomper, apellidoper, emailper, direccionper, telefonoper, usuarioper, contrasenaper, roles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (nombre_usuario, apellido_usuario, email_usuario, direccion_usuario, telefono_usuario, usuario_usuario, contrasena_usuario, roles))
            mysql.connection.commit()
            flash('Usuario registrado satisfactoriamente')
            return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nomper = request.form['nombre_usuario']
        apellidoper = request.form['apellido_usuario']
        emailper = request.form['email_usuario']
        direccionper = request.form['direccion_usuario']
        telefonoper = request.form['telefono_usuario']
        usuarioper = request.form['usuario_usuario']
        contrasenaper = request.form['contrasena_usuario']
        roles = request.form['txtrol']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE personas SET 
                    nomper = %s, 
                    apellidoper = %s, 
                    emailper = %s, 
                    direccionper = %s, 
                    telefonoper = %s, 
                    usuarioper = %s, 
                    contrasenaper = %s,
                    roles = %s
                    WHERE polper = %s""",
                    (nomper, apellidoper, emailper, direccionper, telefonoper, usuarioper, contrasenaper, roles, id))
        mysql.connection.commit()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('index'))


# --------------------------------------------------#
@app.route('/delete/<string:id>')
def delete_usuario(id):
    print("Consulta SQL:", 'DELETE FROM personas WHERE polper = %s' % id)  # Agregar esta línea para imprimir la consulta SQL
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM personas WHERE polper = %s', (id,))
    mysql.connection.commit()
    flash('Usuario removido satisfactoriamente')
    return redirect(url_for('index'))


# ------login----------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_usuario = request.form['usuario'].strip()  # Eliminar espacios en blanco
        contraseña = request.form['contraseña']
        if form_usuario in users and users[form_usuario] == contraseña:
            session['usuario'] = form_usuario
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash(
                'Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')
    return render_template('login.html')


# ---------- canciones ----------#
# Ruta para mostrar las canciones
@app.route('/canciones')
def canciones():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM canciones')
    data = cur.fetchall()
    cur.close()
    return render_template('canciones.html', canciones=data)

# Ruta para agregar una canción
import os

@app.route('/add_cancion', methods=['POST'])
def add_cancion():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_cancion = request.form.get('nombre_cancion')
        nombre_artista = request.form.get('nombre_artista')
        genero_cancion = request.form.get('genero_cancion')
        precio_cancion = request.form.get('precio_cancion')
        duracion_cancion = request.form.get('duracion_cancion')
        año_lanzamiento_cancion = request.form.get('año_lanzamiento_cancion')

        # Verificar si se proporciona una imagen
        if 'imagen_cancion' in request.files:
            imagen_cancion = request.files['imagen_cancion']
            # Guardar la imagen en el servidor
            imagen_path = os.path.join(os.getcwd(), 'static', 'imagenes', imagen_cancion.filename)
            imagen_cancion.save(imagen_path)
            imagen_url = 'static/imagenes/' + imagen_cancion.filename
        else:
            imagen_url = None

        # Verificar campos requeridos
        if nombre_cancion and nombre_artista and genero_cancion and precio_cancion and duracion_cancion and año_lanzamiento_cancion:
            # Crear cursor y ejecutar la consulta
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO canciones (titulo, artista, genero, precio, duracion, alanzamiento, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)', (
                nombre_cancion, nombre_artista, genero_cancion, precio_cancion, duracion_cancion, año_lanzamiento_cancion, imagen_url))

            # Commit y cerrar cursor
            mysql.connection.commit()
            cur.close()

            # Mostrar mensaje flash
            flash('Canción registrada satisfactoriamente', 'success')
        else:
            # Mostrar mensaje flash si falta algún campo requerido
            flash('Todos los campos son obligatorios', 'error')

        # Redirigir a la página de canciones
        return redirect(url_for('canciones'))


# Ruta para eliminar una canción
@app.route('/delete_cancion/<int:cancion_id>', methods=['POST'])
def delete_cancion(cancion_id):
    # Crear cursor
    cur = mysql.connection.cursor()

    # Ejecutar la consulta para eliminar la canción con el ID proporcionado
    cur.execute('DELETE FROM canciones WHERE id = %s', (cancion_id,))

    # Commit y cerrar cursor
    mysql.connection.commit()
    cur.close()

    # Mostrar mensaje flash
    flash('Canción eliminada satisfactoriamente', 'success')

    # Redirigir a la página de canciones
    return redirect(url_for('canciones'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)



   
