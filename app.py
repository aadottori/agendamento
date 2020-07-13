from flask import Flask, render_template, redirect, url_for, request, make_response, session, g, jsonify
import controller
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
import uuid
import json
import formatter
from classes import *  
from operator import itemgetter

app = Flask(__name__)

app.secret_key = "PipocaSalgada"


@app.route('/', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario_inserido = request.form["usuario"]
        senha_inserida = request.form["senha"]

        if controller.verifica_usuario(usuario_inserido):
            user = Usuario(usuario_inserido)

            if user.senha == senha_inserida:
                session["user"] = True
                session["id"] = user.id

                if user.tipo == 1:
                    return redirect(url_for("pagina_profissional"))
                elif user.tipo == 2:
                    return redirect(url_for("pagina_cliente"))
            
            else:
                error = "Senha incorreta."
        
        else:
            error = "Usuário não cadastrado."

    return render_template("login.html", error = error)


@app.route("/pagina_profissional", methods = ["GET", "POST"])
def pagina_profissional():
    error = None
    if "user" in session:
        profissional = Usuario(session["id"])

        if request.method == "POST":
            data = request.form["data"]
            hora = request.form["hora"]

            numero_linhas = controller.numero_linhas_csv("/database/table_horarios.csv")
            add = str(numero_linhas)+","+str(profissional.id)+","+data+","+hora
            controller.adicionar_linha("/database/table_horarios.csv", add)
        return render_template("pagina_profissional.html", error = error)
    
    return redirect(url_for("login"))

