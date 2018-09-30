#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS Equipa")

# Create table as per requirement
sql = """CREATE TABLE `Equipa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (`id`)
);"""

cursor.execute(sql)

# disconnect from server
db.close()
