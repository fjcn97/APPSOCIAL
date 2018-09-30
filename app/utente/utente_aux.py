#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SelectField
from myconnutils import getConnection
from app.utente import bp
from app import create_app
from app.sql.comandos_sql import sql_nome_nome_escalao_preco, sql_utente

app = create_app()

def lista_escaloes():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_nome_nome_escalao_preco)
            escaloes_list_dicts = cursor.fetchall()
        return escaloes_list_dicts

def lista_utentes():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_utente)
            l_dicts_utentes = cursor.fetchall()
            for utente in l_dicts_utentes:
                utente['link'] = url_for('utente.utente',\
                                         user_id=current_user.id,\
                                         email=utente['email'])
    return l_dicts_utentes

class EscalaoPrecoForm(FlaskForm):
    esc_de_preco = SelectField()
