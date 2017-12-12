from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'SBC'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods = ['POST'])
def hello_world():
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
        return jsonify(response = "success", data = str(rv))
    except:
        return jsonify(response = "fail")

@app.route('/setMoney', methods = ['POST'])
def set_money():
    try:
        json = request.get_json()
        id = json["ID_Asistente"]
        creditos = json["creditos"]
        query = "UPDATE ASISTENTE SET creditos = %s WHERE ASISTENTE.ID_Asistente = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[creditos,id])
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
        query = "INSERT INTO ASISTENTE_SALA (ID_Sala, ID_Asistente) VALUES (%s,(SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s)) ;"
        cur = mysql.connection.cursor()
        cur.execute(query,[sala,tag])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        try:
            query = "UPDATE ASISTENTE_SALA SET ID_Sala = %s WHERE ASISTENTE_SALA.ID_Asistente = (SELECT ID_Asistente FROM ASISTENTE WHERE ASISTENTE.TAG = %s);"
            cur = mysql.connection.cursor()
            cur.execute(query,[sala,tag])
            mysql.connection.commit()
            return jsonify(response = "success")
        except:
            return jsonify(response = "fail")

if __name__ == '__main__':
   app.run(debug=True,host= '0.0.0.0')