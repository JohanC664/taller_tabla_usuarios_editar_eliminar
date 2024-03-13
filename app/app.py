from flask import Flask, render_template,request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskusuarios'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

#--------------------------------------------------#
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    return render_template('index.html',usuarioos = data)

#--------------------------------------------------#
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
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO personas (nomper, apellidoper, emailper, direccionper, telefonoper, usuarioper, contrasenaper) VALUES (%s, %s, %s, %s, %s, %s, %s)',(nombre_usuario,apellido_usuario,email_usuario,direccion_usuario,telefono_usuario,usuario_usuario,contrasena_usuario))
        mysql.connection.commit()
        flash('usuario registrado satisfactoriamente')
        return redirect(url_for('index'))
#--------------------------------------------------#
@app.route('/edit/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas WHERE polper = %s',(id))
    data = cur.fetchall()
    return render_template('edit.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nomper = request.form ['nombre_usuario']
        apellidoper = request.form ['apellido_usuario']
        emailper = request.form ['email_usuario']
        direccionper = request.form ['direccion_usuario']
        telefonoper = request.form ['telefono_usuario']
        usuarioper = request.form ['usuario_usuario']
        contrasenaper = request.form ['contrasena_usuario']
        cur= mysql.connection.cursor()
        cur.execute("""UPDATE personas SET 
                    nomper = %s, 
                    apellidoper = %s, 
                    emailper =%s, 
                    direccionper =%s, 
                    telefonoper =%s, 
                    usuarioper =%s, 
                    contrasenaper =%s
                    WHERE polper = %s""", (nomper, apellidoper, emailper, direccionper, telefonoper, usuarioper, contrasenaper, id ))
        mysql.connection.commit()
        flash('Usuario actualizado satisfactoriamnete')
        return redirect(url_for('index'))


#--------------------------------------------------#
@app.route('/delete/<string:id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM personas WHERE polper ={0}'.format(id))
    mysql.connection.commit()
    flash ('Contacto removido satisfactoria mente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)
 


   
