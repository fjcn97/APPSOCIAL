#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from app.equipa.equipa_aux import lista_monitores, lista_monitores_da_equipa,\
     lista_equipas
from flask_login import login_required
from app.equipa import bp
from app.sql.comandos_sql import sql_equipa_nome, sql_equipa_insert,\
     sql_user_equipa_insert, sql_user_equipa_delete,\
     sql_user_equipa_delete_equipa, sql_equipa_delete, sql_fkey_0,\
     sql_equipa_update_nome, sql_user_equipa_update
from app.models import load_equipa

@bp.route('/adicionar_equipa', methods=['GET', 'POST'])
@login_required
def adicionar_equipa():
    with g.db.cursor() as cursor:
        if request.method == "POST":
            nome = request.form.get("nome")
            
            cursor.execute( sql_equipa_nome, (nome) )
            cursor_nome = cursor.fetchone()
            
            if cursor_nome is not None:
                flash("Equipa já existe. Introduza outro nome.")
                return redirect(url_for('equipa.adicionar_equipa'))
            else:   
                cursor.execute( sql_equipa_insert, (nome) )
                g.db.commit()
                flash('Equipa adicionada com sucesso!')
                return redirect(url_for('equipa.equipa',nome=nome))
    return render_template('equipa/adicionar_equipa.html',\
                           title='Adicionar equipa')

@bp.route('/equipa/<nome>/remover_equipa', methods=['GET', 'POST'])
@login_required
def remover_equipa(nome):
    with g.db.cursor() as cursor:
        cursor.execute(sql_user_equipa_delete_equipa, (nome))
        
        cursor.execute(sql_equipa_delete, (nome))
        g.db.commit()
        flash('Equipa removida!')
        return redirect(url_for('equipa.selecionar_equipa'))

@bp.route('/selecionar_equipa', methods=['GET', 'POST'])
@login_required
def selecionar_equipa():
    return render_template('equipa/selecionar_equipa.html',\
                           title='Selecionar equipa',\
                           lista_equipas=lista_equipas())

@bp.route('/equipa/<nome>', methods=['GET', 'POST'])
@login_required
def equipa(nome):
    equipa = load_equipa(nome)
    nome_equipa = equipa.nome
    with g.db.cursor() as cursor:
        if request.method == "POST":
            nome = request.form.get("nome")

            cursor.execute( sql_equipa_nome, (nome) )
            cursor_verificacao = cursor.fetchone()

            if cursor_verificacao is not None:
                flash("Nome já existente. Introduza outro.")
                return redirect(url_for('equipa.equipa', nome=nome))
            else:
                cursor.execute(sql_fkey_0)
                cursor.execute( sql_equipa_update_nome, (nome, nome_equipa) )
                cursor.execute( sql_user_equipa_update, (nome, nome_equipa) )
                g.db.commit()
                flash('Nome alterado com sucesso!')
                return redirect(url_for('equipa.equipa', nome=nome))
    return render_template('equipa/equipa.html', title='Equipa',\
                           equipa = equipa)

@bp.route('/equipa/<nome>/adicionar_monitor', methods=['GET', 'POST'])
@login_required
def adicionar_monitor(nome):
    with g.db.cursor() as cursor:
        if request.method == "POST":
            monitor = request.form.get("monitor")
            cursor.execute( sql_user_equipa_insert, (nome, monitor) )
            g.db.commit()
            flash('Monitor adicionado à equipa!')
            return redirect(url_for('equipa.adicionar_monitor', nome=nome))
    return render_template('equipa/adicionar_monitor.html',\
                           title='Adicionar monitor',\
                           lista_monitores = lista_monitores(nome),\
                           nome = nome)
 
@bp.route('/equipa/<nome>/remover_monitor', methods=['GET', 'POST'])
@login_required
def remover_monitor(nome):
    with g.db.cursor() as cursor:
        if request.method == "POST":
            mon_da_equipa = request.form.get("mon_da_equipa")
            cursor.execute(sql_user_equipa_delete, (nome, mon_da_equipa))
            g.db.commit()
            flash('Monitor removido da equipa!')
            return redirect(url_for('equipa.remover_monitor', nome=nome))
    return render_template('equipa/remover_monitor.html',\
                           title='Remover monitor',\
                           lista_monitores_da_equipa =\
                           lista_monitores_da_equipa(nome),\
                           nome=nome)
