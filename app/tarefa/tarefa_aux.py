#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, url_for
from flask_login import current_user
from myconnutils import getConnection
from app.tarefa import bp
from app import create_app
from app.sql.comandos_sql import sql_visita_utente, sql_categoria_tarefa,\
     sql_nome_tarefa, sql_tarefa_cat_categoria_tarefa,\
     sql_tarefa_visita_tarefa_visita, sql_tarefa_esc_preco

app = create_app()

def lista_categorias_tarefa():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_categoria_tarefa)
            list_dicts_categorias_tarefa = cursor.fetchall()
            return list_dicts_categorias_tarefa

def lista_tarefas():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_nome_tarefa)
            list_dicts_tarefas = cursor.fetchall()
            return list_dicts_tarefas

def lista_tarefas_com_coluna_categoria():
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_tarefa_cat_categoria_tarefa)
            list_dicts_tarefas = cursor.fetchall()
            return list_dicts_tarefas

def lista_tarefas_escs_precos(escalao_preco):
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_tarefa_esc_preco, (escalao_preco))
            list_dicts_tarefas = cursor.fetchall()
            return list_dicts_tarefas
        
def lista_grupos_tarefas(email):
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_visita_utente, (email))
            list_dicts_grupos_tarefas = cursor.fetchall()
            for grupo_tarefas in list_dicts_grupos_tarefas:
                grupo_tarefas['link'] = url_for('tarefa.edit_grupo_tarefas',\
                                                user_id=current_user.id,\
                                                email = email,\
                                                id = grupo_tarefas['id'])
            return list_dicts_grupos_tarefas

def lista_tarefas_visitas(email,grupo_tarefas):
    with app.app_context():
        g.db = getConnection()
        with g.db.cursor() as cursor:
            cursor.execute(sql_tarefa_visita_tarefa_visita, (grupo_tarefas))
            list_dicts_tarefas_visitas = cursor.fetchall()
            for tarefa in list_dicts_tarefas_visitas:
                tarefa['link'] = url_for('tarefa.edit_tarefa_visita',\
                                         user_id=current_user.id,\
                                         email = email,\
                                         id = grupo_tarefas,\
                                         id_tarefa_visita = tarefa['id'])
            
            return list_dicts_tarefas_visitas
