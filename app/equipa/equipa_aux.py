#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, url_for
from myconnutils import getConnection
from app.equipa import bp
from app import create_app
from app.sql.comandos_sql import sql_username_mon, sql_user_equipa_equipa,\
     sql_equipa

app = create_app()

def lista_equipas():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor: 
            cursor.execute(sql_equipa)
            list_dicts_equipas = cursor.fetchall()
            for equipa in list_dicts_equipas:
                equipa['link'] = url_for('equipa.equipa', nome=equipa['nome'])
    return list_dicts_equipas

def lista_monitores(nome):
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor: 
            cursor.execute(sql_username_mon, 'Monitor')
            list_dicts_mons = cursor.fetchall()
            #Não vou adicionar monitores a uma equipa quando estes já existem
            #nesta
    return list(filter(lambda mon: mon not in lista_monitores_da_equipa(nome),\
                   list_dicts_mons))

def lista_monitores_da_equipa(nome):
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor: 
            cursor.execute(sql_user_equipa_equipa, nome)
            list_dicts_mons_da_equipa = cursor.fetchall()
    return list_dicts_mons_da_equipa
