#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0, sql_tabela_precos_insert

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Tabela_precos")

# Create table as per requirement
sql = """CREATE TABLE `Tabela_precos` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome_tarefa` VARCHAR(40) NOT NULL,
    `nome_escalao` VARCHAR(32) NOT NULL,
    `preco` FLOAT NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_tabela_precos_nome_tarefa` FOREIGN KEY (`nome_tarefa`)\
    REFERENCES Tarefa(`nome`),
    CONSTRAINT `FK_tabela_precos_nome_escalao` FOREIGN KEY (`nome_escalao`)\
    REFERENCES Escalao_preco(`nome`)
);"""

cursor.execute(sql)

cursor.execute(sql_tabela_precos_insert,\
               (u'Ida a consulta / tratamento médico', "SemESCALAO", 20.0))
cursor.execute(sql_tabela_precos_insert,\
               (u'Ida a consulta / tratamento médico', "ATE7", 10.3))
cursor.execute(sql_tabela_precos_insert,\
               (u'Ida a consulta / tratamento médico', "ATE14", 15.0))
cursor.execute(sql_tabela_precos_insert,\
               (u'Ida a consulta / tratamento médico', "IDOSOS", 5.0))

cursor.execute(sql_tabela_precos_insert,\
               (u'Deslocação a entidades da comunidade', "SemESCALAO", 10.0))
cursor.execute(sql_tabela_precos_insert,\
               (u'Deslocação a entidades da comunidade', "ATE7", 4.0))
cursor.execute(sql_tabela_precos_insert,\
               (u'Deslocação a entidades da comunidade', "ATE14", 7.5))
cursor.execute(sql_tabela_precos_insert,\
               (u'Deslocação a entidades da comunidade', "IDOSOS", 4.0))

cursor.execute(sql_tabela_precos_insert,\
               ('Transporte regular', "SemESCALAO", 5.5))
cursor.execute(sql_tabela_precos_insert,\
               ('Transporte regular', "ATE7", 3.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Transporte regular', "ATE14", 4.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Transporte regular', "IDOSOS", 3.0))

cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de higiene pessoal', "SemESCALAO", 5.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de higiene pessoal', "ATE7", 3.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de higiene pessoal', "ATE14", 4.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de higiene pessoal', "IDOSOS", 3.1))

cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de imagem', "SemESCALAO", 5.4))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de imagem', "ATE7", 3.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de imagem', "ATE14", 4.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cuidados de imagem', "IDOSOS", 3.0))

cursor.execute(sql_tabela_precos_insert,\
               ('Cabeleireiro', "SemESCALAO", 8.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cabeleireiro', "ATE7", 6.9))
cursor.execute(sql_tabela_precos_insert,\
               ('Cabeleireiro', "ATE14", 7.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Cabeleireiro', "IDOSOS", 5.0))

cursor.execute(sql_tabela_precos_insert,\
               ('Manicure / Pedicure', "SemESCALAO", 12.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Manicure / Pedicure', "ATE7", 8.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Manicure / Pedicure', "ATE14", 10.8))
cursor.execute(sql_tabela_precos_insert,\
               ('Manicure / Pedicure', "IDOSOS", 6.0))

cursor.execute(sql_tabela_precos_insert,\
               ('Barbeiro', "SemESCALAO", 12.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Barbeiro', "ATE7", 8.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Barbeiro', "ATE14", 10.0))
cursor.execute(sql_tabela_precos_insert,\
               ('Barbeiro', "IDOSOS", 6.7))

##cursor.execute(sql_tabela_precos_insert,\
##               (u'Depilação', "SemESCALAO", 12.2))
##cursor.execute(sql_tabela_precos_insert,\
##               (u'Depilação', "ATE7", 8.0))
##cursor.execute(sql_tabela_precos_insert,\
##               (u'Depilação', "ATE14", 10.0))
##cursor.execute(sql_tabela_precos_insert,\
##               (u'Depilação', "IDOSOS", 6.0))

db.commit()

# disconnect from server
db.close()
