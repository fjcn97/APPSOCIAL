#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0, sql_categoria_tarefa_insert

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Categoria_tarefa")

# Create table as per requirement
sql = """CREATE TABLE `Categoria_tarefa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);"""

cursor.execute(sql)

cursor.execute(sql_categoria_tarefa_insert, ("Higiene e conforto pessoal"))
cursor.execute(sql_categoria_tarefa_insert, ("Transporte"))
cursor.execute(sql_categoria_tarefa_insert, ("Alimentação"))
cursor.execute(sql_categoria_tarefa_insert, ("Cuidados com a habitação"))
cursor.execute(sql_categoria_tarefa_insert, ("Cuidados especializados"))
#cursor.execute(sql_categoria_tarefa_insert, ("Outros"))

db.commit()

# disconnect from server
db.close()
