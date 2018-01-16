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
    cur.execute('''SELECT COALESCE(SUM(creditos),0) AS Total_Pagos FROM HISTORIAL_CREDITOS WHERE modo_pago = 1''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT (COALESCE(SUM(creditos),0)/COUNT(ID_Asistente)) AS Media_Creditos FROM ASISTENTE''')
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
    cur.execute('''SELECT COALESCE(SUM(creditos),0) AS Total_Creditos FROM ASISTENTE''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT COALESCE(SUM(creditos),0) AS Total_Pagos FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE() AND modo_pago = 1''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT (SUM(creditos)/COUNT(ID_Asistente)) AS Media_Creditos FROM ASISTENTE''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT *,COALESCE(Total_Creditos_Hoy/Total_Creditos_Ayer*100,0) AS Incremento_Ventas FROM (SELECT COALESCE(SUM(creditos),0) AS Total_Creditos_Hoy FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE() AND modo_pago=1) AS HOY JOIN (SELECT COALESCE(SUM(creditos),0) AS Total_Creditos_Ayer FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE()-1 AND modo_pago=1) AS AYER''')
    rv = cur.fetchone()
    data.update({"Incremento_Ventas":float(rv["Incremento_Ventas"])})
    data.update({"Total_Creditos_Hoy":float(rv["Total_Creditos_Hoy"])})
    data.update({"Total_Creditos_Ayer":float(rv["Total_Creditos_Ayer"])})
    cur.execute('''SELECT COALESCE(SUM(creditos),0) AS Total_Cargas FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE() AND modo_pago = 0''')
    rv = cur.fetchone()
    data.update(rv)
    cur.execute('''SELECT SUM(creditos) AS Cargas, HOUR(hora) AS Hora FROM (SELECT creditos, hora FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE() AND modo_pago=0) AS CARGAS''')
    rv = cur.fetchall()
    for r in rv:
        if r["Cargas"] != None:
            r["Cargas"]=float(r["Cargas"])
        else:
            r["Cargas"]=""
            r["Hora"]=""
    data.update({"Datos_Cargas":rv})
    cur.execute('''SELECT SUM(creditos) AS Pagos, HOUR(hora) AS Hora FROM (SELECT creditos, hora FROM HISTORIAL_CREDITOS WHERE DATE(hora) = CURDATE() AND modo_pago=1) AS PAGOS''')
    rv = cur.fetchall()
    for r in rv:
        print(r["Pagos"])
        if r["Pagos"] != None:
            r["Pagos"]=float(r["Pagos"])
        else:
            r["Pagos"]=""
            r["Hora"]=""
    data.update({"Datos_Pagos":rv})
    cur.execute('''SELECT ASISTENTE.Nombre, ASISTENTE.Apellidos, ASISTENTE.DNI, HISTORIAL_CREDITOS.hora, HISTORIAL_CREDITOS.creditos, HISTORIAL_CREDITOS.modo_pago FROM HISTORIAL_CREDITOS JOIN ASISTENTE  ON HISTORIAL_CREDITOS.ID_Asistente = ASISTENTE.ID_Asistente''')
    rv = cur.fetchall()
    data.update({"Movimientos":rv})
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
        movimiento = json["movimiento"]
        query = "UPDATE ASISTENTE SET Creditos = %s WHERE ASISTENTE.ID_Asistente = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[creditos,id])
        query = "INSERT INTO HISTORIAL_CREDITOS (ID_Asistente, creditos, modo_pago) VALUES (%s,%s,%s)"
        cur.execute(query,[id,movimiento,modoPago])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        return jsonify(response = "fail")

@app.route('/tryAccess', methods = ['POST'])
def try_access():
    try:
        json = request.get_json()
        tag = json["TAG"]
        idSala = json["ID_Sala"]
        query = "SELECT Nivel_Acceso, Aforo_Act, Aforo_Max FROM SALA WHERE ID_Sala = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[idSala])
        sala = cur.fetchone()
        nivelAccesoSala = sala.get("Nivel_Acceso")
        aforoActSala = sala.get("Aforo_Act")
        aforoMaxSala = sala.get("Aforo_Max")
        query = "SELECT Nivel_Acceso, ID_Asistente FROM ASISTENTE WHERE TAG = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[tag])
        asistente = cur.fetchone()
        nivelAccesoAsistente = asistente.get("Nivel_Acceso")
        idAsistente = asistente.get("ID_Asistente")
        if (nivelAccesoSala>nivelAccesoAsistente):
            return jsonify(response = "fail", error= "Nivel de acceso insuficiente")
        if (aforoActSala+1>aforoMaxSala):
            return jsonify(response = "fail", error= "Se ha alcanzado el aforo maximo")
        query = "INSERT INTO ASISTENTE_SALA (ID_Sala, ID_Asistente) VALUES (%s,%s) ;"
        cur = mysql.connection.cursor()
        cur.execute(query,[idSala,idAsistente])
        query = "INSERT INTO HISTORIAL (ID_Sala, ID_Asistente) VALUES (%s,%s) ;"
        cur.execute(query,[idSala,idAsistente])
        query = "UPDATE SALA SET Aforo_Act = %s WHERE ID_Sala = %s ;"
        cur.execute(query,[aforoActSala+1, idSala])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        try:
            query = "UPDATE ASISTENTE_SALA SET ID_Sala = %s WHERE ASISTENTE_SALA.ID_Asistente = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query,[idSala,idAsistente])
            mysql.connection.commit()
            if(cur.rowcount == 0):
                return jsonify(response = "fail", error= "El asistenete ya esta en la sala")
            else:
                query = "UPDATE HISTORIAL SET Hora_Salida = NOW() WHERE HISTORIAL.ID_Asistente = %s AND HISTORIAL.Hora_Salida IS NULL ;"
                cur.execute(query,[idAsistente])
                query = "INSERT INTO HISTORIAL (ID_Sala, ID_Asistente) VALUES (%s,%s) ;"
                cur.execute(query,[idSala,idAsistente])
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
        query = "UPDATE SALA SET Aforo_Act = Aforo_Act -1 WHERE ID_Sala = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,[id])
        mysql.connection.commit()
        return jsonify(response = "success")
    except:
        return jsonify(response = "fail", error="Ha ocurrido un error")

if __name__ == '__main__':
   app.run(debug=True,host= '0.0.0.0',port=5000)