from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF8')

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'SBC'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#############Views##################

@app.route('/')
def index():
    return render_template('index.html',data = getDataDashboard())

def getDataDashboard():
    data = {}
    cur = mysql.connection.cursor()
    cur.execute('''SELECT COUNT(ID_Asistente) AS Total_Asistentes FROM ASISTENTE''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT COUNT(*) AS Total_Accesos FROM HISTORIAL''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT COALESCE(SUM(creditos),0) AS Total_Pagos FROM HISTORIAL_CREDITOS WHERE modo_pago = 1''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute(''' SELECT AVG(Sum_Asistentes) AS Media_Asistentes FROM (SELECT COALESCE(Sum_Asistentes,0) AS Sum_Asistentes , SALA.ID_Sala FROM SALA LEFT JOIN (SELECT COUNT(ID_Asistente) AS Sum_Asistentes, ID_Sala FROM ASISTENTE_SALA) AS SUMAS ON SALA.ID_Sala = SUMAS.ID_Sala) AS SUMAS''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute(''' SELECT Nombre, (Aforo_Act/Aforo_Max*100) AS Porcentaje_Aforo FROM SALA ORDER BY Porcentaje_Aforo DESC LIMIT 4''')
    rv = cur.fetchall()
    data.update({"Top_Salas":rv})
    cur.execute('''SELECT COUNT(ID_Asistente) AS Entradas, HOUR(Hora_Entrada) AS Hora FROM (SELECT ID_Asistente, Hora_Entrada FROM HISTORIAL WHERE DATE(Hora_Entrada) = CURDATE()) AS ENTRADAS GROUP BY HOUR(Hora_Entrada) ORDER BY HOUR(Hora_Entrada)''')
    rv = cur.fetchall()
    data.update({"Datos_Entradas":rv})
    cur.execute('''SELECT COUNT(ID_Asistente) AS Salidas, HOUR(Hora_Salida) AS Hora FROM (SELECT ID_Asistente, Hora_Salida FROM HISTORIAL WHERE DATE(Hora_Salida) = CURDATE()) AS SALIDAS GROUP BY HOUR(Hora_Salida) ORDER BY HOUR(Hora_Salida)''')
    rv = cur.fetchall()
    data.update({"Datos_Salidas":rv})
    now = datetime.datetime.now()
    data.update({"Fecha": now.strftime("%A, %d %B")})
    cur.execute('''SELECT ID_Sala, Nombre AS Nombre_Sala FROM SALA''')
    rv = cur.fetchall()
    data.update({"Sidebar":rv})
    return data


@app.route('/sala/<id>')
def sala(id):
    return render_template('sala.html', data = getDataSala(id))

def getDataSala(id):
    data = {}
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM SALA WHERE ID_Sala = %s''',(id))
    rv = cur.fetchone()
    data.update({"Sala":rv})
    cur.execute('''SELECT COUNT(*) AS Accesos_Hoy FROM HISTORIAL WHERE ID_Sala = %s AND DATE(Hora_Entrada) = CURDATE()''',(id))
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT AVG(Tiempo) AS Tiempo_Medio FROM (SELECT (timestampdiff(MINUTE,Hora_Entrada,Hora_Salida)) AS Tiempo FROM HISTORIAL WHERE ID_Sala = %s) AS TIEMPOS''',(id))
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT (Aforo_Act/Aforo_Max*100) AS Porcentaje_Aforo FROM SALA WHERE ID_Sala = %s''',(id))
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT Aforo_Act, (Aforo_Max-SALA.Aforo_Act) AS Aforo_Restante FROM SALA WHERE ID_Sala = %s''',(id))
    rv = cur.fetchone()
    data.update({"Aforo":rv})
    cur.execute('''SELECT COUNT(ID_Asistente) AS Entradas, HOUR(Hora_Entrada) AS Hora FROM (SELECT ID_Asistente, Hora_Entrada FROM HISTORIAL WHERE DATE(Hora_Entrada) = CURDATE() AND ID_Sala = %s) AS ENTRADAS GROUP BY HOUR(Hora_Entrada) ORDER BY HOUR(Hora_Entrada)''',(id))
    rv = cur.fetchall()
    data.update({"Datos_Entradas":rv})
    cur.execute('''SELECT COUNT(ID_Asistente) AS Salidas, HOUR(Hora_Salida) AS Hora FROM (SELECT ID_Asistente, Hora_Salida FROM HISTORIAL WHERE DATE(Hora_Salida) = CURDATE() AND ID_Sala = %s) AS SALIDAS GROUP BY HOUR(Hora_Salida) ORDER BY HOUR(Hora_Salida)''',(id))
    rv = cur.fetchall()
    data.update({"Datos_Salidas":rv})
    cur.execute('''SELECT Nombre, Apellidos, DNI, Hora_Entrada, Hora_Salida FROM HISTORIAL JOIN ASISTENTE A ON HISTORIAL.ID_Asistente = A.ID_Asistente WHERE ID_Sala = %s''',(id))
    rv = cur.fetchall()
    data.update({"Accesos":rv})
    cur.execute('''SELECT ID_Sala, Nombre AS Nombre_Sala FROM SALA''')
    rv = cur.fetchall()
    data.update({"Sidebar":rv})
    return data

@app.route('/asistentes')
def asistentes():
    return render_template('asistentes.html', data = getDataAsistentes())

def getDataAsistentes():
    data = {}
    cur = mysql.connection.cursor()
    cur.execute('''SELECT COUNT(ID_Asistente) AS Total_Asistentes FROM ASISTENTE''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT (Asistentes_En_Sala/Asistentes*100) AS Porcentaje_En_Sala FROM (SELECT COUNT(ASISTENTE_SALA.ID_Asistente) AS Asistentes_En_Sala, COUNT(ASISTENTE.ID_Asistente) AS Asistentes FROM ASISTENTE_SALA RIGHT JOIN ASISTENTE ON ASISTENTE_SALA.ID_Asistente = ASISTENTE.ID_Asistente) AS COUNTS_ASISTENTES''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT SUM(creditos) AS Total_Pagos FROM HISTORIAL_CREDITOS WHERE modo_pago = 1''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT (SUM(creditos)/COUNT(ID_Asistente)) AS Media_Creditos FROM ASISTENTE''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT Nombre, Apellidos, DNI, Nivel_Acceso, creditos FROM ASISTENTE''')
    rv = cur.fetchall()
    data.update({"Asistentes":rv})
    cur.execute('''SELECT ID_Sala, Nombre AS Nombre_Sala FROM SALA''')
    rv = cur.fetchall()
    data.update({"Sidebar":rv})
    return data

@app.route('/transacciones')
def transacciones():
    return render_template('transacciones.html', data = getDataTransacciones())

def getDataTransacciones():
    data = {}
    cur = mysql.connection.cursor()
    cur.execute('''SELECT ID_Sala, Nombre AS Nombre_Sala FROM SALA''')
    rv = cur.fetchall()
    data.update({"Sidebar":rv})
    return data

#################API#################

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
        query = "SELECT Nivel_Acceso FROM SALA WHERE ID_Sala = %s;"#TODO: ver el aforo
        cur = mysql.connection.cursor()
        cur.execute(query,[sala])
        nivelAccesoSala = cur.fetchone().get("Nivel_Acceso")
        query = "SELECT Nivel_Acceso FROM ASISTENTE WHERE TAG = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag])
        nivelAccesoAsistente = cur.fetchone().get("Nivel_Acceso")
        if (nivelAccesoSala>nivelAccesoAsistente):#TODO: comprobar el aforo
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