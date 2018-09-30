#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash
from app.auth import bp
from app.sql.comandos_sql import sql_user_username

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    with g.db.cursor() as cursor:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            cursor.execute(sql_user_username, (username))
            user_dict = cursor.fetchone()
            if user_dict is None or not\
               check_password_hash(user_dict['password_hash'], password):
                flash('Username e/ou password inválido(s).')
                return redirect(url_for('auth.login'))
            user = User(user_dict['id'], user_dict['username'],\
                        user_dict['nome'], user_dict['telemovel'],\
                        user_dict['email'], user_dict['categoria'],\
                        user_dict['nivel_de_acesso'],\
                        user_dict['password_hash'])
            login_user(user) #remember=form.remember.data
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('auth/login.html', title="Login")

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
