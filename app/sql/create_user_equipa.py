#!/usr/bin/python

import myconnutils
from comandos_sql import sql_fkey_0

# Open database connection
db = myconnutils.getConnection()

# prepare a cursor object using cursor() method
cursor = db.cursor()

cursor.execute(sql_fkey_0)

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS User_Equipa")

# Create table as per requirement
sql = """CREATE TABLE `User_Equipa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `equipa` VARCHAR(30),
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_user_equipa_equipa` FOREIGN KEY (`equipa`) REFERENCES\
    Equipa(`nome`),
    CONSTRAINT `FK_user_equipa_monitor` FOREIGN KEY (`username`) REFERENCES\
    User(`username`)
);"""

cursor.execute(sql)

# disconnect from server
db.close()
