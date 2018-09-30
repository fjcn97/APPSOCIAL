#!/usr/bin/python
# -*- coding: utf-8 -*-

import myconnutils
from comandos_sql import sql_fkey_0, sql_tarefa_insert

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Tarefa")

# Create table as per requirement
sql = """CREATE TABLE `Tarefa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) UNIQUE NOT NULL,
  `categoria` int NOT NULL,
  `tarifa` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tbl_Categoria_tarefa_fk` (`categoria`),
  CONSTRAINT `tbl_Categoria_tarefa_fk` FOREIGN KEY (`categoria`)\
  REFERENCES `Categoria_tarefa` (`id`)
);"""

cursor.execute(sql)

cursor.execute(sql_tarefa_insert,\
               (u'Ida a consulta / tratamento médico', 1, 'Fixa'))
cursor.execute(sql_tarefa_insert,\
               (u'Deslocação a entidades da comunidade', 1, 'Horária'))
cursor.execute(sql_tarefa_insert, ('Transporte regular',1, 'Fixa'))

cursor.execute(sql_tarefa_insert, ('Cuidados de higiene pessoal',2, 'Fixa'))
cursor.execute(sql_tarefa_insert, ('Cuidados de imagem',2, 'Fixa'))
cursor.execute(sql_tarefa_insert, ('Cabeleireiro',2, 'Fixa'))
cursor.execute(sql_tarefa_insert, ('Manicure / Pedicure',2, 'Fixa'))
cursor.execute(sql_tarefa_insert, ('Barbeiro',2, 'Fixa'))
cursor.execute(sql_tarefa_insert, ('Depilação',2, 'Fixa'))

cursor.execute(sql_tarefa_insert,\
               (u'Fornecimento e apoio nas refeições, respeitando as dietas com prescrição médica',3, 'Fixa'))
cursor.execute(sql_tarefa_insert,\
               (u'Confeção de alimentos no domicílio',3, 'Fixa'))

cursor.execute(sql_tarefa_insert,('Limpezas ao domicílio',4, 'Horária'))
cursor.execute(sql_tarefa_insert,(u'Lavandaria/engomadoria',4, 'Fixa'))
cursor.execute(sql_tarefa_insert, (u'Pequenas reparações',4, 'Fixa'))
cursor.execute(sql_tarefa_insert,\
               (u'Aquisição de bens e géneros alimentícios',4, 'Fixa'))

cursor.execute(sql_tarefa_insert, (u'Apoio a acamados',5, 'Horária'))
cursor.execute(sql_tarefa_insert,\
               (u'Fisioterapia/Terapia ocupacional',5, 'Horária'))
cursor.execute(sql_tarefa_insert, ('Enfermagem',5, 'Fixa'))
cursor.execute(sql_tarefa_insert, (u'Consultas ao domicílio',5, 'Fixa'))
cursor.execute(sql_tarefa_insert, (u'Psicologia',5, 'Fixa'))
cursor.execute(sql_tarefa_insert,\
               (u'Ações de formação para familiares e cuidadores',5, 'Horária'))

##cursor.execute(sql_tarefa_insert, (u'Companhia / conversação',6, 'Horária'))
##cursor.execute(sql_tarefa_insert, (u'Leituras',6, 'Horária'))
##cursor.execute(sql_tarefa_insert, ('Animação socio-cultural',6, 'Horária'))
##cursor.execute(sql_tarefa_insert, (u'Acompanhamento em passeios',6, 'Horária'))
##cursor.execute(sql_tarefa_insert, (u'Passear o animal de estimação',6, 'Fixa'))

db.commit()

# disconnect from server
db.close()
