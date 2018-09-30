#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Utente")

# Create table as per requirement
sql = """CREATE TABLE `Utente` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(64) NOT NULL,
    `email` VARCHAR(30) NOT NULL UNIQUE,
    `telemovel` VARCHAR(9) NOT NULL UNIQUE,
    `morada` VARCHAR(64) NOT NULL,
    `nome_a_contactar` VARCHAR(64),
    `num_a_contactar` VARCHAR(9),
    `med_fam_apoio` varchar(64),
    `alergias` varchar(64),
    `doencas` varchar(64),
    `esc_de_preco` VARCHAR(32) NOT NULL,
    `comentarios` TEXT,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_utente_escalao_preco` FOREIGN KEY (`esc_de_preco`)\
    REFERENCES Escalao_preco(`nome`)
);"""

cursor.execute(sql)

# disconnect from server
db.close()
