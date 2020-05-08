from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()
app = Flask(__name__)



@app.route('/esprimo/<numero>')
def esprimo(numero):
    if int(numero) < 2:     #si es menos que 2 no es primo, por lo tanto devolverá Falso
        return ("No es primo")
    for i in range(2, int(numero)):  #un rango desde el dos hasta el numero que nosotros elijamos
        if int(numero) % i == 0:    #si el resto da 0 no es primo, por lo tanto devuelve Falso
            return ("No es primo")
    return ("Es primo")

@app.route('/login/<username>/<password>')
def login(username, password):
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    for i in range(len(users)):
        if(users[i].username== username and users[i].password == password ):
            return "Username and password exist"
    return "Fail!"

@app.route('/create_user/<nombre>/<apellido>/<user>/<clave>')
def create_user(nombre,apellido,user,clave):
    user = entities.User(
        name = nombre,
        fullname = apellido,
        username = user,
        password = clave
    )
    print(user)
    #Persistir de un
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()
    return "User Created!"

@app.route('/read_users/')
def read_users():
    #Para conversar con la base de datos
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    respuestadatos= " "
    for i in range(len(users)):
        respuestadatos += "<br> Username: </b>" + str(users[i].username) +"<br> Nombre: </b>" + str(users[i].name) +"<br> Fullname: </b>" + str(users[i].fullname) +"<br> Password: </b>: "+str(users[i].password) +"<br>"
    return respuestadatos
    
@app.route('/palindrome/<palabra>')
def palindrome(palabra):
    if len(palabra) == 1: return ("Si")
    if palabra[0] != palabra[-1]: return ("No")
    return palindrome(palabra[1:-1])

@app.route('/multiplo/<numero1>/<numero2>')
def multiplo(numero1,numero2):
    resto = int(numero1) % int(numero2)
    if resto ==0:
        return ("Si es")
    else:
        return ("No es ")

@app.route('/nombre/<escribe>')
def nombre(escribe):
    return (escribe)

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)




if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
