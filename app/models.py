from flask import g
from app import login_manager
from flask_login import UserMixin
from app.sql.comandos_sql import sql_user_id, sql_utente_email, sql_visita_id,\
     sql_tarefa_visita_id, sql_equipa_nome

class User(UserMixin):
    def __init__(self, id, username, nome, telemovel, email, categoria,\
                 nivel_de_acesso, password):
        self.id = id
        self.username = username
        self.nome = nome
        self.telemovel = telemovel
        self.email = email
        self.categoria = categoria
        self.nivel_de_acesso = nivel_de_acesso
        self.password = password

@login_manager.user_loader
def load_user(id):
    cursor = g.db.cursor()
    cursor.execute(sql_user_id, id)
    user_dict = cursor.fetchone()
    return User(id, user_dict['username'], user_dict['nome'],\
                    user_dict['telemovel'], user_dict['email'],\
                    user_dict['categoria'], user_dict['nivel_de_acesso'],\
                    user_dict['password_hash'])

class Utente():
    def __init__(self, id, nome, email, telemovel, morada, nome_a_contactar,\
                 num_a_contactar, med_fam_apoio, alergias, doencas,\
                 esc_de_preco, comentarios):
        self.id = id
        self.nome = nome
        self.email = email
        self.telemovel = telemovel
        self.morada = morada
        self.nome_a_contactar = nome_a_contactar
        self.num_a_contactar = num_a_contactar
        self.med_fam_apoio = med_fam_apoio
        self.alergias = alergias
        self.doencas = doencas
        self.esc_de_preco = esc_de_preco
        self.comentarios = comentarios

def load_utente(email):
    cursor = g.db.cursor()
    cursor.execute(sql_utente_email, (email))
    utente_dict = cursor.fetchone()
    utente = Utente(utente_dict['id'], utente_dict['nome'], email,\
                    utente_dict['telemovel'], utente_dict['morada'],\
                    utente_dict['nome_a_contactar'],\
                    utente_dict['num_a_contactar'],\
                    utente_dict['med_fam_apoio'],\
                    utente_dict['alergias'],\
                    utente_dict['doencas'],\
                    utente_dict['esc_de_preco'],\
                    utente_dict['comentarios'])
    return utente
     
class Equipa():
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

def load_equipa(nome):
    cursor = g.db.cursor()
    cursor.execute(sql_equipa_nome, (nome))
    equipa_dict = cursor.fetchone()
    return Equipa(equipa_dict['id'], nome)

class Visita():
    def __init__(self, id, nome, descricao, utente):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.utente = utente

def load_visita(id):
    cursor = g.db.cursor()
    cursor.execute(sql_visita_id, (id))
    visita_dict = cursor.fetchone()
    return Visita(int(id), visita_dict['nome'], visita_dict['descricao'],\
                    visita_dict['utente'])

class Tarefa_Visita():
    def __init__(self, id, title, duracao_esperada, start,\
                 hora_minutos_inicial, end, hora_minutos_final, preco,\
                 visita):
        self.id = id
        self.title = title 
        self.duracao_esperada = duracao_esperada
        self.start = start
        self.hora_minutos_inicial = hora_minutos_inicial
        self.end = end
        self.hora_minutos_final = hora_minutos_final
        self.preco = preco
        self.visita = visita

def load_tarefa_visita(id):
    cursor = g.db.cursor()
    cursor.execute(sql_tarefa_visita_id, (id))
    tarefa_visita_dict = cursor.fetchone()
    return Tarefa_Visita(id,\
                        tarefa_visita_dict['title'],\
                        tarefa_visita_dict['duracao_esperada'],\
                        tarefa_visita_dict['start'],\
                        tarefa_visita_dict\
                        ['hora_minutos_inicial'],\
                        tarefa_visita_dict['end'],\
                        tarefa_visita_dict\
                        ['hora_minutos_final'],\
                        tarefa_visita_dict['preco'],\
                        tarefa_visita_dict['visita'])
