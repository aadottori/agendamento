import random
import mysql.connector
from flask import render_template, make_response
import pdfkit
from datetime import date, datetime, timedelta
import validador
import formatter
from classes import *

config = {
  'user': 'root',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'agendador',
  'port': '3306'}

con = mysql.connector.connect(**config)
cursor = con.cursor()


#==Funções básicas==#

def select(fields, tables, where = None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT " + fields + " FROM " +tables
        
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()


def select_last(id_profissional, id_cliente):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()

        id_profissional = str(id_profissional)
        id_cliente = str(id_cliente)
        loc = select("MAX(data_consulta)","table_atendimentos", f'id_cliente = {id_cliente} and id_profissional = {id_profissional}')

        selectionados = id_cliente+', data_consulta, '+id_profissional
        query = f'SELECT * FROM table_atendimentos WHERE id_cliente = "{id_cliente}" and id_profissional = "{id_profissional}" and data_consulta = "{str(loc[0][0])}" and tipo_atendimento = Plano' 
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        con.close()


def exist(cpf, table):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "SELECT COUNT(nome) FROM " + table +" WHERE cpf="+cpf
        cursor.execute(query)
        return bool(cursor.fetchall()[0][0])
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


def insert(values, table, fields = None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "INSERT INTO " +table
        if (fields):
            query += " ("+ fields + ") "
        query += " VALUES " + ",".join(["("+v+")" for v in values])
        cursor.execute(query)
        con.commit()
        
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


def update(sets, table, where):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "UPDATE " +table
        query += " SET " + ",".join([field+ " = '" + value + "'" for field, value in sets.items()])
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        con.close()


def delete(table, where):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "DELETE FROM "+ table +" WHERE "+where
        cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


def delete_cell(column, table, where):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        query = "UPDATE "+ table + " SET " + column + " = NULL WHERE " + where
        cursor.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()  


def select_CursorDict(fields, tables, where = None):
    con = None
    cursor = None
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        cursor = con.cursor(dictionary = True) 
        query = "SELECT " + fields + " FROM " +tables
        if (where):
            query += " WHERE " + where
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        
    finally:
        cursor.close()
        con.close()


#==Funções derivadas==#

def verifica_usuario(cpf):
    """retorna True se o usuario já está cadastrado e False c.c."""
    usuario = "usuario="+str(usuario)
    return bool(len(select("usuario", "table_usuarios", usuario)))

