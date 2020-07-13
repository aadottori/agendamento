from flask import Flask, render_template, redirect, url_for, request, make_response, session, g, jsonify
import controller
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
import uuid
import json
import validador
import formatter
from classes import *  
from operator import itemgetter

app = Flask(__name__)

app.secret_key = "PipocaSalgada"

@app.route('/', methods=["GET", "POST"]
def login():
    error = None
    if request.method == "POST":
        usuario_inserido = request.form["usuario"]
        senha_inserida = request.form["senha"]

        usuario = Usuario(usuario_in)
