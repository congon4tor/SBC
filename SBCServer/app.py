from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
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

@app.route('/new', methods = ['POST'])
def new_user():
    try:
        json = request.get_json()
        dni = json["DNI"]
        tag = json["TAG"]
        nombre = json["Nombre"]
        apellidos = json["Apellidos"]
        nivel = json["Nivel_Acceso"]
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO ASISTENTE (ID_Asistente, DNI, TAG, Nombre, Apellidos, Nivel_Acceso) VALUES (NULL,%s,%s,%s,%s,%s)''',(dni,tag,nombre,apellidos,nivel))
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        return jsonify(response = "fail")

if __name__ == '__main__':
   app.run(debug=True)