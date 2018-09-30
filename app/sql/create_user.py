#!/usr/bin/python
# -*- coding: utf-8 -*-

import myconnutils
from comandos_sql import sql_fkey_0, sql_user_insert
## Executando diretamente este ficheiro, aparecia uma mensagem a dizer
## "No module named 'werkzeug'" (pelo menos, no computador no qual trabalhei,
## que, por omissão do sistema, usava o pip do python2, em vez do python3.
## Assim sendo, este módulo só dava para ser instalado no sistema,
## através do pip. Portanto, o python3 não consegue aceder a este módulo,
## visto que usa o pip3. Logo, ou se executava este ficheiro com o python2
## ou, então, com o ambiente virtual aberto e acedendo à pasta onde se
## encontra este ficheiro. Desta forma, já se podia executar com o python3.
from werkzeug.security import generate_password_hash

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)
    
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS User")

# Create table as per requirement
sql = """CREATE TABLE `User` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL UNIQUE,
    `nome` VARCHAR(64) NOT NULL,
    `telemovel` VARCHAR(9) NOT NULL UNIQUE,
    `email` varchar(30) NOT NULL UNIQUE,
    `categoria` VARCHAR(32) NOT NULL,
    `nivel_de_acesso` VARCHAR(32) NOT NULL,
    `password_hash` varchar(128) NOT NULL,
    PRIMARY KEY (`id`)
);"""

cursor.execute(sql)

##Inserir administrador (obrigatório!).
##Senão, "'NoneType' object is not subscriptable"...
cursor.execute(sql_user_insert,('admin', 'Fábio Nogueira', 916524412,\
                    'admin@appsocial.com', 'Outro', 'Administrador',\
                    generate_password_hash('admin')))

db.commit()

# disconnect from server
db.close()
