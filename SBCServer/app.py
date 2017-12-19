from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'SBC'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listUsers', methods = ['POST'])
def list_users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM ASISTENTE''')
    rv = cur.fetchall()
    return jsonify(data = str(rv),response="success")

@app.route('/newUser', methods = ['POST'])
def new_user():
    try:
        json = request.get_json()
        dni = json["DNI"]
        tag = generate_password_hash(dni)
        nombre = json["Nombre"]
        apellidos = json["Apellidos"]
        nivel = json["Nivel_Acceso"]
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO ASISTENTE (ID_Asistente, DNI, TAG, Nombre, Apellidos, Nivel_Acceso) VALUES (NULL,%s,%s,%s,%s,%s)''',(dni,tag,nombre,apellidos,nivel))
        mysql.connection.commit()
        return jsonify(response = "success", TAG = tag)
    except:
        return jsonify(response = "fail")

@app.route('/findUser', methods = ['POST'])
def find_user():
    try:
        json = request.get_json()
        tag = json["TAG"]
        query = "SELECT * FROM ASISTENTE WHERE TAG = %s"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag])
        rv = cur.fetchone()
        if (rv==None):
            return jsonify(response = "fail")
        return jsonify(response = "success", data = str(rv))
    except:
        return jsonify(response = "fail")

@app.route('/setMoney', methods = ['POST'])
def set_money():
    try:
        json = request.get_json()
        id = json["ID_Asistente"]
        creditos = json["creditos"]
        modoPago = json["modo_pago"]
        query = "UPDATE ASISTENTE SET creditos = %s WHERE ASISTENTE.ID_Asistente = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[creditos,id])
        query = "INSERT INTO HISTORIAL_CREDITOS (ID_Asistente, creditos, modo_pago) VALUES (%s,%s,%s)"
        cur.execute(query,[id,creditos,modoPago])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        return jsonify(response = "fail")

@app.route('/tryAccess', methods = ['POST'])
def try_access():
    try:
        json = request.get_json()
        tag = json["TAG"]
        sala = json["ID_Sala"]
        query = "SELECT Nivel_Acceso FROM SALA WHERE ID_Sala = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[sala])
        nivelAccesoSala = cur.fetchone().get("Nivel_Acceso")
        query = "SELECT Nivel_Acceso FROM ASISTENTE WHERE TAG = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag])
        nivelAccesoAsistente = cur.fetchone().get("Nivel_Acceso")
        if (nivelAccesoSala>nivelAccesoAsistente):
            return jsonify(response = "fail", error= "Nivel de acceso insuficiente")
        query = "INSERT INTO ASISTENTE_SALA (ID_Sala, ID_Asistente) VALUES (%s,(SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s)) ;"
        cur = mysql.connection.cursor()
        cur.execute(query,[sala,tag])
        query = "INSERT INTO HISTORIAL (ID_Sala, ID_Asistente) VALUES (%s,(SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s)) ;"
        cur.execute(query,[sala,tag])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        try:
            query = "UPDATE ASISTENTE_SALA SET ID_Sala = %s WHERE ASISTENTE_SALA.ID_Asistente = (SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s);"
            cur = mysql.connection.cursor()
            cur.execute(query,[sala,tag])
            mysql.connection.commit()
            if(cur.rowcount == 0):
                return jsonify(response = "fail", error= "El asistenete ya esta en la sala")
            else:
                query = "UPDATE HISTORIAL SET Hora_Salida = NOW() WHERE HISTORIAL.ID_Asistente = (SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s) AND HISTORIAL.Hora_Salida IS NULL ;"
                cur.execute(query,[tag])
                query = "INSERT INTO HISTORIAL (ID_Sala, ID_Asistente) VALUES (%s,(SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s)) ;"
                cur.execute(query,[sala,tag])
                mysql.connection.commit()
                return jsonify(response = "success")
        except:
            return jsonify(response = "fail", error="Ha ocurrido un error")

@app.route('/exitRoom', methods = ['POST'])
def exit_room():
    try:
        json = request.get_json()
        tag = json["TAG"]
        id = json["ID_Sala"]
        query = "UPDATE HISTORIAL SET Hora_Salida = NOW() WHERE HISTORIAL.ID_Asistente = (SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s) AND HISTORIAL.ID_Sala = %s AND HISTORIAL.Hora_Salida IS NULL;"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag,id])
        query = "DELETE FROM ASISTENTE_SALA WHERE ASISTENTE_SALA.ID_Asistente = (SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s);"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        return jsonify(response = "fail", error="Ha ocurrido un error")

if __name__ == '__main__':
   app.run(debug=True,host= '0.0.0.0')