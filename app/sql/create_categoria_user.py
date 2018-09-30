#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0, sql_categoria_user_insert

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Categoria_user")

# Create table as per requirement
sql = """CREATE TABLE `Categoria_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);"""

cursor.execute(sql)

cursor.execute(sql_categoria_user_insert, ("Enfermeiro"))
cursor.execute(sql_categoria_user_insert, ("Médico"))
cursor.execute(sql_categoria_user_insert, ("Auxiliar"))
cursor.execute(sql_categoria_user_insert, ("Condutor"))
#cursor.execute(sql_categoria_user_insert, ("Outro"))

db.commit()

# disconnect from server
db.close()
