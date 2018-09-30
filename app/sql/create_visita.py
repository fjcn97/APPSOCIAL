#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Visita")

# Grupo de tarefas associado a um utente
sql = """CREATE TABLE `Visita` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(40) NOT NULL UNIQUE,
    `descricao` VARCHAR(64),
    `utente` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_visita_utente`\
    FOREIGN KEY (`utente`) REFERENCES Utente(`email`)
);"""

cursor.execute(sql)

# disconnect from server
db.close()
