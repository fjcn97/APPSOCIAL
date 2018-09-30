#!/usr/bin/env python

from myconnutils import getConnection
from comandos_sql import sql_fkey_0

# Open database connection
db = getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Tarefa_Visita")

# Create table as per requirement
sql = """CREATE TABLE `Tarefa_Visita` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(40),
    `preco` FLOAT,
    `duracao_esperada` VARCHAR(6),
    `start` VARCHAR(10),
    `hora_minutos_inicial` VARCHAR(5),
    `end` VARCHAR(10),
    `hora_minutos_final` VARCHAR(5),
    `visita` INT NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_tarefa_visita_tarefa`\
    FOREIGN KEY (`title`) REFERENCES Tarefa(`nome`),
    CONSTRAINT `FK_tarefa_visita_visita`\
    FOREIGN KEY (`visita`) REFERENCES Visita(`id`)
);"""
##title: title em vez de nome, para depois o FullCalendar reconhecer como um
##evento
##start: VARCHAR em vez de DATE para depois o valor deste campo poder
##ser serializado em JSON e, consequentemente, as tarefas entrarem no
##calendário
##duracao_esperada: VARCHAR em vez de TIME, porque, assim, é inserido sem
##os segundos; e 6 porque as horas poderão ter até 3 dígitos (máx.: 999)
cursor.execute(sql)

# disconnect from server
db.close()
