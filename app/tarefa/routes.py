#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from flask_weasyprint import HTML, render_pdf
from app.tarefa.tarefa_aux import lista_grupos_tarefas, lista_tarefas_visitas,\
     lista_categorias_tarefa, lista_tarefas, lista_tarefas_com_coluna_categoria,\
     lista_tarefas_escs_precos
from app.utente.utente_aux import lista_escaloes
from flask_login import login_required
from app.models import load_visita, load_utente, load_tarefa_visita, load_user
from app.tarefa import bp
from app.sql.comandos_sql import sql_visita_nome, sql_visita_insert,\
     sql_visita_id, sql_visita_update, sql_visita_utente,\
     sql_tarefa_visita_insert, sql_tabela_precos_tarefa_escalao,\
     sql_tarefa_visita_update,\
     sql_tarefa_visita_calendario, sql_utente_email,\
     sql_tarefa_visita_visita_start, sql_tarefa_insert, sql_tarefa_nome,\
     sql_categoria_tarefa_nome, sql_categoria_tarefa_insert,\
     sql_tarefa_visita_tarefa_visita, sql_tabela_precos,\
     sql_tabela_precos_insert, sql_tarefa_visita_nome_escalao,\
     sql_escalao_preco_nome, sql_escalao_preco_insert
from app.main.routes import hoje, equipas_do_user
import json, datetime

@bp.route('/adicionar_categoria_tarefa', methods=['GET', 'POST'])
@login_required
def adicionar_categoria_tarefa():    
    with g.db.cursor() as cursor: 
        if request.method == 'POST':
            nome = request.form.get('nome')

            cursor.execute(sql_categoria_tarefa_nome, (nome))
            categoria_tarefa_dict = cursor.fetchone()

            if categoria_tarefa_dict is not None:
                flash("Categoria já existe. Introduza outra.")
                return redirect(url_for('tarefa.adicionar_categoria_tarefa'))
            else:
                cursor.execute(sql_categoria_tarefa_insert, (nome))

                g.db.commit()

                flash('Categoria de tarefas adicionada com sucesso!')
                return redirect(url_for('tarefa.adicionar_categoria_tarefa'))
        
    return render_template('tarefa/adicionar_categoria_tarefa.html',\
                           title='Adicionar categoria de tarefas')

@bp.route('/adicionar_escalao_preco', methods=['GET', 'POST'])
@login_required
def adicionar_escalao_preco():
    with g.db.cursor() as cursor:
        if request.method == 'POST':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
        
            cursor.execute(sql_escalao_preco_nome, (nome))
            cursor_nome = cursor.fetchone()
            
            if cursor_nome is not None:
                flash("Escalão de preço já existe. Introduza outro.")
                return redirect(url_for('tarefa.adicionar_escalao_preco'))
            else:
                cursor.execute( sql_escalao_preco_insert,\
                               (nome,descricao) )
                g.db.commit()
                flash('Escalão de preço adicionado com sucesso!')
                return redirect(url_for('main.index'))
    return render_template('tarefa/adicionar_escalao_preco.html',\
                           title='Adicionar escalão de preço')

@bp.route('/adicionar_preco', methods=['GET', 'POST'])
@login_required
def adicionar_preco():    
    with g.db.cursor() as cursor: 
        if request.method == 'POST':
            nome_tarefa = request.form.get('nome_tarefa')
            nome_escalao = request.form.get('nome_escalao')
            preco = request.form.get('preco')

            cursor.execute(sql_tabela_precos_tarefa_escalao,\
                           (nome_tarefa, nome_escalao))
            tarefa_escalao_dict = cursor.fetchone()

            if tarefa_escalao_dict is not None:
                flash("Combinação entre tarefa e escalão já existe.\
                      Introduza outra.")
                return redirect(url_for('tarefa.adicionar_preco'))
            else:
                cursor.execute(sql_tabela_precos_insert,\
                               (nome_tarefa, nome_escalao, preco))

                g.db.commit()

                flash('Preço adicionado com sucesso!')
                return redirect(url_for('tarefa.adicionar_preco'))
        
    return render_template('tarefa/adicionar_preco.html',\
                           title='Adicionar preço',\
                           lista_tarefas=lista_tarefas(),\
                           lista_escaloes=lista_escaloes())

@bp.route('/tabela_de_precos',  methods=['GET', 'POST'])
@login_required
def tabela_de_precos():
    with g.db.cursor() as cursor:
        cursor.execute(sql_tabela_precos)
        tarifas_list_dicts = cursor.fetchall()
        
    return render_template('tarefa/tabela_de_precos.html',\
                           title='Tabela de preços',\
                           tarifas_list_dicts =\
                           tarifas_list_dicts)

@bp.route('/adicionar_tarefa', methods=['GET', 'POST'])
@login_required
def adicionar_tarefa():    
    with g.db.cursor() as cursor: 
        if request.method == 'POST':
            nome = request.form.get('nome')
            categoria_tarefa = request.form.get('categoria_tarefa')
            tarifa = request.form.get('tarifa')

            cursor.execute(sql_tarefa_nome, (nome))
            tarefa_dict = cursor.fetchone()

            if tarefa_dict is not None:
                flash("Tarefa já existe. Introduza outra.")
                return redirect(url_for('tarefa.adicionar_tarefa'))
            else:
                cursor.execute(sql_tarefa_insert, (nome, categoria_tarefa,\
                                                   tarifa))

                g.db.commit()

                flash('Tarefa adicionada com sucesso!')
                return redirect(url_for('tarefa.adicionar_tarefa'))
        
    return render_template('tarefa/adicionar_tarefa.html',\
                           title='Adicionar tarefa',\
                           lista_categorias_tarefa=lista_categorias_tarefa())

@bp.route('/user_id/<user_id>/utente/<email>/visita', methods=['GET', 'POST'])
@login_required
def visita(user_id,email):
    user = load_user(user_id)
    utente = load_utente(email)
    email_utente = utente.email
    esc_de_preco_utente = utente.esc_de_preco
    
    with g.db.cursor() as cursor:
        if request.method == 'POST':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            
            cursor.execute(sql_visita_nome, (nome))
            grupo_tarefas_dict = cursor.fetchone()

            if grupo_tarefas_dict is not None:
                flash("Nome atribuído já existe. Introduza outro.")
                return redirect(url_for('tarefa.visita',\
                                        user_id=user_id,email=email))
            else:
                cursor.execute(sql_visita_insert,\
                               (nome, descricao, email))

                cursor.execute(sql_visita_nome, (nome))
                grupo_tarefas = cursor.fetchone()
                id_grupo_tarefas = grupo_tarefas['id']

                sem_duracao_esperada = "00:00"
                data_hora_inicio_fim_vazias = ""
                
                for tarefa in lista_tarefas_escs_precos(esc_de_preco_utente):
                    tarefa_selecionada = request.form.get(tarefa['nome'])
                    if (tarefa_selecionada != None):
                        if tarefa['tarifa'] == "Horária":
                            tarefa['preco'] = 0.0
                            
                        cursor.execute(sql_tarefa_visita_insert,\
                                       (tarefa['nome'], sem_duracao_esperada,\
                                        data_hora_inicio_fim_vazias,\
                                        data_hora_inicio_fim_vazias,\
                                        data_hora_inicio_fim_vazias,\
                                        data_hora_inicio_fim_vazias,
                                        tarefa['preco'], id_grupo_tarefas))

                g.db.commit()

                flash('Conjunto adicionado com sucesso!')
                return redirect(url_for('tarefa.selecionar_tarefa',\
                                        user_id=user_id, email=email,\
                                        id=id_grupo_tarefas))
        
    return render_template('tarefa/visita.html',\
                           title='Novo grupo de tarefas', utente=utente,\
                           user=user, user_equipas = equipas_do_user(user_id),\
                           lista_tarefas_escs_precos=\
                           lista_tarefas_escs_precos(esc_de_preco_utente))

@bp.route('/user_id/<user_id>/utente/<email>/selecionar_grupo_tarefas',\
          methods=['GET', 'POST'])
@login_required
def selecionar_grupo_tarefas(user_id,email):
    user = load_user(user_id)
    utente = load_utente(email)
    return render_template('tarefa/selecionar_grupo_tarefas.html',\
                           title='Selecionar grupo de tarefas',
                           user=user, utente = utente, lista_grupos_tarefas=\
                           lista_grupos_tarefas(email))

@bp.route('/user_id/<user_id>/utente/<email>/edit_grupo_tarefas/<id>',  methods=['GET', 'POST'])
@login_required
def edit_grupo_tarefas(user_id, email, id):
    user = load_user(user_id)
    utente = load_utente(email)
    grupo_tarefas = load_visita(id)
    
    with g.db.cursor() as cursor:
        preco_total = 0
        
        l_datas_inicio = []
        l_datas_fim = []
        l_duracoes_esperadas = []

        #Nesta função, também fiz o JOIN da tarifa para o cálculo do preço
        #total
        for tarefa in lista_tarefas_visitas(email, id):
            preco_total += tarefa['preco']
            
            if tarefa['start'] != '' and\
               tarefa['hora_minutos_inicial'] != '':
                tarefa['start']+= " "
                date_time_inicial = tarefa['start']+\
                                    tarefa['hora_minutos_inicial']
                l_datas_inicio.append(date_time_inicial)
                
            elif tarefa['start'] != '' and\
               tarefa['hora_minutos_inicial'] == '':
                l_datas_inicio.append(tarefa['start'])
        
            l_duracoes_esperadas.append(tarefa['duracao_esperada'])
            date_time_final = tarefa['end'] + " " + tarefa['hora_minutos_final']

            try:
                datetime.datetime.strptime(date_time_final,\
                                           "%Y-%m-%d %H:%M")
                l_datas_fim.append(date_time_final)
            except ValueError:
                continue
        
        duracao_total = datetime.timedelta()
        
        for duracao in l_duracoes_esperadas:
            (h, m) = duracao.split(':')
            dur_repartida = datetime.timedelta(hours=int(h), minutes=int(m))
            duracao_total += dur_repartida
        
        l_datas_inicio.sort()
        l_datas_fim.sort()
        
        if request.method == "POST":
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            
            cursor.execute(sql_visita_nome, (nome))
            grupo_tarefas_dict = cursor.fetchone()
            
            if grupo_tarefas_dict is not None and grupo_tarefas.nome !=\
               nome:
                flash("Nome atribuído já existe. Introduza outro.")
                return redirect(url_for('tarefa.edit_grupo_tarefas',\
                                        user_id=user_id,email=email,\
                                        id=id))
            elif nome == "":
                flash("A sério? Que tal introduzir um grupo de tarefas com nome?")
                return redirect(url_for('tarefa.edit_grupo_tarefas',\
                                        user_id=user_id,email=email,\
                                        id=id))
            else:
                cursor.execute(sql_visita_update,\
                               (nome, descricao, grupo_tarefas.id))
                g.db.commit()
                    
                flash('Grupo de tarefas alterado com sucesso!')
                return redirect(url_for('tarefa.edit_grupo_tarefas',\
                                        user_id=user_id,email=email,\
                                        id=id))

    return render_template('tarefa/edit_grupo_tarefas.html',\
                           title='Editar grupo de tarefas: ' +\
                           grupo_tarefas.nome,\
                           grupo_tarefas = grupo_tarefas,\
                           utente = utente,\
                           preco_total = preco_total,\
                           l_datas_inicio = l_datas_inicio,\
                           l_datas_fim = l_datas_fim,\
                           #os segundos não interessam...
                           duracao_total = str(duracao_total)[:-3],\
                           user=user)

@bp.route('/user_id/<user_id>/utente/<email>/edit_grupo_tarefas/<id>/selecionar_tarefa',\
          methods=['GET', 'POST'])
@login_required
def selecionar_tarefa(user_id, email, id):
    user = load_user(user_id)
    utente = load_utente(email)
    grupo_tarefas = load_visita(id)

    return render_template('tarefa/selecionar_tarefa.html',\
                           title='Selecionar tarefa',
                           utente = utente, grupo_tarefas =\
                           grupo_tarefas,user=user,\
                           lista_tarefas_visitas=\
                           lista_tarefas_visitas(email,id))

@bp.route('/user_id/<user_id>/utente/<email>/edit_grupo_tarefas/<id>/edit_tarefa_visita/<id_tarefa_visita>',\
          methods=['GET', 'POST'])
@login_required
def edit_tarefa_visita(user_id, email, id, id_tarefa_visita):
    user = load_user(user_id)
    utente = load_utente(email)
    grupo_tarefas = load_visita(id)
    tarefa_visita = load_tarefa_visita(id_tarefa_visita)

    with g.db.cursor() as cursor:
        if request.method == "POST":
            tempo_medio_horas = request.form.get('tempo_medio_horas')
            tempo_medio_minutos = request.form.get('tempo_medio_minutos')
            start = request.form.get('start')
            hora_minutos_inicial = request.form.get('hora_minutos_inicial')

            #Se se introduzir as horas com o formato 00x ou 0xx, com x <= 9,
            #o primeiro 0 é cortado
            #1º if
            if len(tempo_medio_horas) == 3 and tempo_medio_horas[0] == '0':
                tempo_medio_horas = tempo_medio_horas[1:]

            #Se não se introduzir nada no campo das horas
            if (tempo_medio_horas == ''):
                tempo_medio_horas = "00"

            #Se não se introduzir nada no campo dos minutos
            if (tempo_medio_minutos == ''):
                tempo_medio_minutos = "00"

            tempo_medio_minutos_ajustado = ""
            tempo_medio_horas_ajustado = ""

            date_time_final = datetime.timedelta()

            #Caso a data e a hora iniciais não sejam vazias, estas são juntas
            #para o cálculo da data e hora finais
            if start != '' and hora_minutos_inicial != '':
                start+= " "
                date_time_inicial = start+\
                                    hora_minutos_inicial
                date_time_final = datetime.datetime.strptime\
                            (date_time_inicial, "%Y-%m-%d %H:%M")

            #Caso se introduza as horas com o formato 0x, com x <= 9,
            #ou o primeiro if lá de cima faça com que as horas venham
            #neste formato, só permanece o 2º dígito (05 -> 5)
            if tempo_medio_horas != "00" and int(tempo_medio_horas) < 10 and\
               len(tempo_medio_horas) > 1:
                tempo_medio_horas_ajustado = "0" +\
                                               tempo_medio_horas[1]
            #Caso se introduza as horas com o formato x, com x <= 9,
            #não se corta nada
            elif tempo_medio_horas != "00" and int(tempo_medio_horas) < 10 and\
                 len(tempo_medio_horas) == 1:
                tempo_medio_horas_ajustado = "0" +\
                                               tempo_medio_horas
            else:
                tempo_medio_horas_ajustado = tempo_medio_horas

            #Caso se introduza os minutos com o formato 0x, com x <= 9,
            #só permanece o 2º dígito (05 -> 5)  
            if tempo_medio_minutos != "00" and int(tempo_medio_minutos) < 10\
               and len(tempo_medio_minutos) == 2:
                tempo_medio_minutos_ajustado = ":0" +\
                                               tempo_medio_minutos[1]
            elif tempo_medio_minutos != "00" and int(tempo_medio_minutos) < 10\
                 and len(tempo_medio_minutos) == 1:
                tempo_medio_minutos_ajustado = ":0" +\
                                               tempo_medio_minutos
            else:
                tempo_medio_minutos_ajustado = ":" +\
                                               tempo_medio_minutos
                
            duracao_esperada = tempo_medio_horas_ajustado +\
                               tempo_medio_minutos_ajustado
            
            horas, minutos = map(int, duracao_esperada.split(':'))
            dur_str_to_timedelta = datetime.timedelta\
                                 (hours = horas, minutes = minutos)
            
            date_time_final += dur_str_to_timedelta
            date_time_final = str(date_time_final)

            #Se a data e a hora iniciais existirem, o data_time_final terá este
            #formato
            try:
                datetime.datetime.strptime\
                                        (date_time_final,\
                                         "%Y-%m-%d %H:%M:%S")
                date_time_final = date_time_final.split(' ')

                end = date_time_final[0]
                #Não me interessam os segundos
                hora_minutos_final = date_time_final[1][:-3]

            #Basta uma destas não existir, para o seu formato não corresponder
            #Logo, o fim é indeterminado
            except ValueError:
                end = ""
                hora_minutos_final = ""

            cursor.execute(sql_tarefa_visita_nome_escalao,\
                           (tarefa_visita.id, utente.esc_de_preco))
            dict_tarefa_visita = cursor.fetchone()

            #Para o cálculo do preço da tarefa influenciado pelo número de horas
            #e pelo escalão da pessoa, caso a sua tarifa seja "Horária"
            if duracao_esperada and\
               dict_tarefa_visita['tarifa'] == "Horária":
                preco = horas * dict_tarefa_visita['preco_original']
            else:
                preco = dict_tarefa_visita['preco_original']
                    
            cursor.execute(sql_tarefa_visita_update,\
                           (duracao_esperada,\
                            start, hora_minutos_inicial,\
                            end, hora_minutos_final,\
                            preco,\
                            tarefa_visita.id))
    
            g.db.commit()
                
            flash('Tarefa alterada com sucesso!')
            return redirect(url_for('tarefa.selecionar_tarefa',\
                                    user_id=user_id,\
                                    email=email,\
                                    id=id))
            
    return render_template('tarefa/edit_tarefa_visita.html',\
                           title='Editar tarefa: ' + tarefa_visita.title,\
                           grupo_tarefas = grupo_tarefas,\
                           utente = utente, tarefa_visita =\
                           tarefa_visita,user=user)

@bp.route('/user_id/<user_id>/utente/<email>/historico_de_tarefas',\
          methods=['GET', 'POST'])
@login_required
def historico_de_tarefas(user_id,email):
    user = load_user(user_id)
    utente = load_utente(email)
    with g.db.cursor() as cursor:
        cursor.execute(sql_visita_utente, (email))
        l_tarefas = []
        
        for grupo_tarefas in cursor.fetchall():
            cursor.execute(sql_tarefa_visita_tarefa_visita,\
                           (grupo_tarefas['id']))
            l_dicts_tarefas = cursor.fetchall()
            
            for dict_tarefa in l_dicts_tarefas:    
                date_time_final = dict_tarefa['end'] + " " +\
                                      dict_tarefa['hora_minutos_final']
                
                try:
                    datetime.datetime.strptime\
                                            (date_time_final,\
                                             "%Y-%m-%d %H:%M")
                    if date_time_final < str(datetime.datetime.now()):
                        l_tarefas.append(dict_tarefa)
                except ValueError:
                    continue

    return render_template('tarefa/historico_de_tarefas.html',\
                           l_tarefas = l_tarefas, utente=utente,\
                           title="Histórico de tarefas",user=user)

def tarefas_hoje(): 
    with g.db.cursor() as cursor:
        #Para a coluna utente da tabela Visita ficar junta à tabela
        #Tarefa_Visita...
        cursor.execute(sql_tarefa_visita_visita_start, hoje)
        l_tarefas = cursor.fetchall()
        
        for tarefa in l_tarefas:
            date_time_final = tarefa['end'] + " " + tarefa['hora_minutos_final']
            
            try:
                datetime.datetime.strptime\
                                        (date_time_final,\
                                         "%Y-%m-%d %H:%M")
            except ValueError:
                tarefa['hora_minutos_inicial'] = "-"
                tarefa['end'] = "-"
                tarefa['hora_minutos_final'] = "-"

        return l_tarefas

@bp.route('/ver_tarefas_hoje')
@login_required
def ver_tarefas_hoje():
    return render_template('tarefa/ver_tarefas_hoje.html',\
                           title='Tarefas de hoje',\
                           l_tarefas=tarefas_hoje())

@bp.route('/lista_tarefas_hoje.pdf')
@login_required
def lista_tarefas_hoje_pdf():
    html = render_template('tarefa/lista_tarefas_hoje.html',\
                           l_tarefas=tarefas_hoje())

    return render_pdf(HTML(string=html),\
                      download_filename="lista_tarefas_hoje.pdf")

@bp.route('/user_id/<user_id>/calendario', methods=['GET', 'POST'])
def calendario(user_id):
    user = load_user(user_id)
    return render_template('tarefa/calendario.html', title='Calendário', user=\
                           user, user_equipas=equipas_do_user(user.username),\
                           lista_categorias_tarefa = lista_categorias_tarefa())

## Ver http://flask.pocoo.org/docs/0.12/api/#module-flask.json para outros
## módulos interessantes do flask json
## start e end são serializados em JSON
@bp.route('/user_id/<user_id>/eventos')
def eventos(user_id):
    with g.db.cursor() as cursor:
        cursor.execute(sql_tarefa_visita_calendario)

        l_tarefas_com_inicio = []
        for tarefa in cursor.fetchall():
            cursor.execute(sql_visita_id, tarefa['visita'])
            email_utente = cursor.fetchone()['utente']
            cursor.execute(sql_utente_email, email_utente)
            nome_utente = cursor.fetchone()['nome']
            tarefa['title'] += " - " + nome_utente
            
            if tarefa['start'] != '' and tarefa['hora_minutos_inicial'] != '':
                tarefa['start'] += " " + \
                                  tarefa['hora_minutos_inicial']
                tarefa['end'] += " " + \
                                  tarefa['hora_minutos_final']
                l_tarefas_com_inicio.append(tarefa)
            elif tarefa['start'] != '' and tarefa['hora_minutos_inicial'] == '':
                l_tarefas_com_inicio.append(tarefa)

        return json.dumps(l_tarefas_com_inicio)
