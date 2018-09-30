#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
import json
from app.utente.utente_aux import lista_escaloes, lista_utentes,\
     EscalaoPrecoForm
from flask_login import login_required
from app.models import load_utente, load_user
from app.utente import bp
from app.sql.comandos_sql import sql_utente_email, sql_utente_telemovel,\
     sql_utente_insert, sql_utente_update, sql_utente_comentarios
from app.main.routes import equipas_do_user

@bp.route('/adicionar_utente', methods=['GET', 'POST'])
@login_required
def adicionar_utente():
    form = EscalaoPrecoForm()
    lista_escaloes_tuplos = list(map(lambda dict_escalao:\
                                 tuple(dict_escalao.values()),\
                                 lista_escaloes()))
    form.esc_de_preco.choices = lista_escaloes_tuplos
    
    with g.db.cursor() as cursor:
        if request.method == 'POST':
            nome = request.form.get('nome')
            morada = request.form.get('morada')
            telemovel = request.form.get('telemovel')
            email = request.form.get('email')
            esc_de_preco = request.form.get('esc_de_preco')
            med_fam_apoio = request.form.get('med_fam_apoio')
            alergias = request.form.get('alergias')
            doencas = request.form.get('doencas')
            nome_a_contactar = request.form.get('nome_a_contactar')
            num_a_contactar = request.form.get('num_a_contactar')
            
            cursor.execute(sql_utente_telemovel, (telemovel))
            cursor_telefone = cursor.fetchone()

            cursor.execute(sql_utente_email, (email))
            cursor_email = cursor.fetchone()
            
            if cursor_telefone is not None:
                flash("Nº de telemóvel já existe. Introduza outro.")
                return redirect(url_for('utente.adicionar_utente'))
            if cursor_email is not None:
                flash("Email já existe. Introduza outro.")
                return redirect(url_for('utente.adicionar_utente'))
            else:
                if nome_a_contactar == "" or num_a_contactar == "":
                    nome_a_contactar = None
                    num_a_contactar = None
                cursor.execute( sql_utente_insert, (nome, email,\
                                                    telemovel, morada,\
                                                    nome_a_contactar,\
                                                    num_a_contactar,\
                                                    med_fam_apoio, alergias,\
                                                    doencas, esc_de_preco) )
                g.db.commit()
                flash('Utente adicionado com sucesso!')
                return redirect(url_for('main.index'))
    return render_template('utente/adicionar_utente.html',\
                           title='Adicionar utente', form = form)

@bp.route('/selecionar_utente', methods=['GET', 'POST'])
@login_required
def selecionar_utente():
    return render_template('utente/selecionar_utente.html',\
                           title='Selecionar utente',
                           lista_utentes=lista_utentes())

@bp.route('/user_id/<user_id>/utente/<email>', methods=['GET', 'POST'])
@login_required
def utente(user_id, email):
    user = load_user(user_id)
    utente = load_utente(email)
    with g.db.cursor() as cursor:
        if request.method == "POST":
            comentarios = request.form.get("comentarios")
            cursor.execute(sql_utente_comentarios, (comentarios,\
                                                    utente.email))
            g.db.commit()
            flash('Guardado!')
            return redirect(url_for('utente.utente', user_id=user_id,\
                                    email=email))
    return render_template('utente/utente.html', utente=utente,\
                           title='Perfil do utente', user_equipas =\
                           equipas_do_user(user.username), user=user)

@bp.route('/user_id/<user_id>/utente/<email>/edit_utente_profile',\
          methods=['GET', 'POST'])
@login_required
def edit_utente_profile(user_id,email):
    user = load_user(user_id)
    utente = load_utente(email)
    form = EscalaoPrecoForm(obj=utente)

    lista_escaloes_tuplos = list(map\
                                (lambda dict_escalao:\
                                 tuple(dict_escalao.values()),\
                                 lista_escaloes()))
    form.esc_de_preco.choices = lista_escaloes_tuplos
    
    with g.db.cursor() as cursor:
        if request.method == "POST":
            morada = request.form.get("morada")
            telemovel = request.form.get("telemovel")
            email = request.form.get("email")
            esc_de_preco = request.form.get("esc_de_preco")
            med_fam_apoio = request.form.get("med_fam_apoio")
            alergias = request.form.get("alergias")
            doencas = request.form.get("doencas")
            nome_a_contactar = request.form.get("nome_a_contactar")
            num_a_contactar = request.form.get("num_a_contactar")
            
            cursor.execute(sql_utente_telemovel, (telemovel))
            cursor_telemovel = cursor.fetchone()

            cursor.execute(sql_utente_email, (email))
            cursor_email = cursor.fetchone()
            
            if cursor_telemovel is not None and str(utente.telemovel) !=\
               str(telemovel):
                flash("Nº já existe. Introduza outro.")
                return redirect(url_for('utente.edit_utente_profile',\
                                        user_id=user_id,email=email))
            if cursor_email is not None and utente.email != email:
                flash("Email já existe. Introduza outro.")
                return redirect(url_for('utente.edit_utente_profile',\
                                        user_id=user_id,email=email))
            else:
                if nome_a_contactar == "" or num_a_contactar == "":
                    nome_a_contactar = None
                    num_a_contactar = None
                    
                cursor.execute(sql_utente_update, (telemovel, email, morada,\
                                                   nome_a_contactar,\
                                                   num_a_contactar,\
                                                   esc_de_preco,\
                                                   med_fam_apoio,\
                                                   alergias, doencas,\
                                                   utente.email))
                g.db.commit()
                flash('Alterações guardadas!')
                return redirect(url_for('utente.utente', user_id=user_id,\
                                        email=email))
    return render_template('utente/edit_utente_profile.html',\
                           title='Editar perfil do utente',\
                           utente=utente,form=form, user=user)

@bp.route('/utente/<email>/ver_ficha_clinica')
@login_required
def ver_ficha_clinica(email):
    utente = load_utente(email)
    return render_template('utente/ver_ficha_clinica.html', utente=utente,\
                           title="Ficha clínica")

@bp.route("/utentes")
def utentes():
    text = request.args['searchText']
    
    result = list(filter\
                 (lambda utente: text.lower() in utente['nome'].lower(),\
                  lista_utentes()))

    return json.dumps({"results":result})
