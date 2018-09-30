#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from app.main.main_aux import CategoriaForm
from flask_login import login_required, current_user
from app.models import User, load_user
from werkzeug.security import generate_password_hash
from app.main import bp
from app.sql.comandos_sql import sql_user_username, sql_user_telemovel,\
     sql_user_email, sql_user_insert, sql_user_update, sql_user_equipa_mon,\
     sql_user, sql_nome_nome_categoria_user, sql_categoria_user_insert,\
     sql_categoria_user_nome
from datetime import datetime

hoje = datetime.utcnow().strftime("%Y-%m-%d")
hoje_monitor = datetime.utcnow().strftime("%d/%m/%Y")

def equipas_do_user(username):
    with g.db.cursor() as cursor:
        cursor.execute(sql_user_equipa_mon, username)
        user_equipas = cursor.fetchall()
    return user_equipas

def lista_categorias_user():
    with g.db.cursor() as cursor:
        cursor.execute(sql_nome_nome_categoria_user)
        list_dicts_categorias_user = cursor.fetchall()
    return list_dicts_categorias_user

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Bem-vindo, ' +\
                           current_user.nome, hoje_monitor=\
                           hoje_monitor, user_equipas=\
                           equipas_do_user(current_user.username))

@bp.route('/adicionar_categoria_user', methods=['GET', 'POST'])
@login_required
def adicionar_categoria_user():    
    with g.db.cursor() as cursor: 
        if request.method == 'POST':
            nome = request.form.get('nome')

            cursor.execute(sql_categoria_user_nome, (nome))
            categoria_user_dict = cursor.fetchone()

            if categoria_user_dict is not None:
                flash("Categoria já existe. Introduza outra.")
                return redirect(url_for('main.adicionar_categoria_user'))
            else:
                cursor.execute(sql_categoria_user_insert, (nome))

                g.db.commit()

                flash('Categoria de utilizadores adicionada com sucesso!')
                return redirect(url_for('main.adicionar_categoria_user'))
        
    return render_template('user/adicionar_categoria_user.html',\
                           title='Adicionar categoria de utilizadores')

@bp.route('/adicionar_user', methods=['GET', 'POST'])
@login_required
def adicionar_user():
    form = CategoriaForm()
    lista_categorias_user_tuplos = list(map(lambda dict_categoria_user:\
                                 tuple(dict_categoria_user.values()),\
                                 lista_categorias_user()))
    form.categoria.choices = lista_categorias_user_tuplos
    
    with g.db.cursor() as cursor:
        if request.method == 'POST':
            username = request.form.get('username')
            nome = request.form.get('nome')
            telemovel = request.form.get('telemovel')
            email = request.form.get('email')
            categoria = request.form.get('categoria')
            nivel_de_acesso = request.form.get('nivel_de_acesso')
            password = request.form.get('password')
            
            cursor.execute(sql_user_username, (username))
            cursor_username = cursor.fetchone()
            
            cursor.execute(sql_user_telemovel, (telemovel))
            cursor_telemovel = cursor.fetchone()

            cursor.execute(sql_user_email, (email))
            cursor_email = cursor.fetchone()
            
            if cursor_username is not None:
                flash("Nome de utilizador já existe. Introduza outro.")
                return redirect(url_for('main.adicionar_user'))
            if cursor_telemovel is not None:
                flash("Nº de telemóvel já existe. Introduza outro.")
                return redirect(url_for('main.adicionar_user'))
            if cursor_email is not None:
                flash("Email já existe. Introduza outro.")
                return redirect(url_for('main.adicionar_user'))
            else:
                cursor.execute(sql_user_insert, ( username, nome,\
                                                 telemovel, email,\
                                                 categoria, nivel_de_acesso,\
                                                 generate_password_hash\
                                                  (password) ) )
                g.db.commit()
                flash('Utilizador adicionado com sucesso!')
                return redirect(url_for('main.index'))
    return render_template('user/adicionar_user.html',\
                           title='Adicionar utilizador',\
                           form=form)

@bp.route('/ver_users', methods=['GET', 'POST'])
@login_required
def ver_users():
    with g.db.cursor() as cursor:
        cursor.execute(sql_user)
        l_dicts_users = cursor.fetchall()
    
    return render_template('user/ver_users.html',\
                           title='Ver utilizadores',\
                           l_dicts_users=l_dicts_users)

@bp.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = load_user(id)
    form = CategoriaForm(obj=user)
    lista_categorias_user_tuplos = list(map(lambda dict_categoria_user:\
                                 tuple(dict_categoria_user.values()),\
                                 lista_categorias_user()))
    form.categoria.choices = lista_categorias_user_tuplos
    
    with g.db.cursor() as cursor:
        if request.method == "POST":
            telemovel = request.form.get("telemovel")
            email = request.form.get("email")
            categoria = request.form.get("categoria")

            cursor.execute(sql_user_telemovel, (telemovel))
            cursor_telemovel = cursor.fetchone()

            cursor.execute(sql_user_email, (email))
            cursor_email = cursor.fetchone()

            if cursor_telemovel is not None and str(user.telemovel)\
               != str(telemovel):
                flash("Nº de telemóvel já existe. Introduza outro.")
                return redirect(url_for('main.user', id=id))

            if cursor_email is not None and user.email !=\
               email:
                flash("Email já existe. Introduza outro.")
                return redirect(url_for('main.user', id=id))
            else:
                cursor.execute(sql_user_update,\
                               (telemovel, email,\
                                categoria, user.email))
                g.db.commit()
                flash('Alterações guardadas!')
                return redirect(url_for('main.user', id=id))
    return render_template('user/user.html', user=user, user_equipas =\
                           equipas_do_user(user.username), form = form,\
                           title='Utilizador: ' + user.username)
