#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0, sql_escalao_preco_insert

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Escalao_preco")

# Create table as per requirement
sql = """CREATE TABLE `Escalao_preco` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(32) NOT NULL UNIQUE,
    `descricao` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`id`)
);"""

cursor.execute(sql)

cursor.execute(sql_escalao_preco_insert,('SemESCALAO', 'Sem escalão'))
cursor.execute(sql_escalao_preco_insert,\
               ('ATE7', 'Crianças até aos 7 anos (inclusive)'))
cursor.execute(sql_escalao_preco_insert,\
               ('ATE14', 'Crianças dos 8 aos 14 anos (inclusive)'))
##cursor.execute(sql_escalao_preco_insert, ('IDOSOS', '65 ou +'))

db.commit()

# disconnect from server
db.close()
