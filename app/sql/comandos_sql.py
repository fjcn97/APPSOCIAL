sql_fkey_0 = "SET FOREIGN_KEY_CHECKS=0;"

## Comandos Tarefa_Visita
sql_tarefa_visita_id = "SELECT * FROM Tarefa_Visita WHERE id = %s;"
sql_tarefa_visita_title = "SELECT * FROM Tarefa_Visita WHERE title = %s;"

sql_tarefa_visita_calendario = "SELECT Tarefa_Visita.*,\
                                  Tarefa.tarifa, Tarefa.categoria,\
                                  Categoria_tarefa.nome AS categoria_nome\
                                  FROM Tarefa_Visita\
                                  INNER JOIN Tarefa\
                                  ON Tarefa_Visita.title=Tarefa.nome\
                                  INNER JOIN Categoria_tarefa\
                                  ON Tarefa.categoria=Categoria_tarefa.id;"

sql_tarefa_visita_insert = "INSERT INTO Tarefa_Visita\
                           (`title`, `duracao_esperada`, `start`,\
                           `hora_minutos_inicial`, `end`, `hora_minutos_final`,\
                           `preco`, `visita`)\
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

sql_tarefa_visita_update = "UPDATE Tarefa_Visita SET duracao_esperada = %s,\
                           start = %s,\
                           hora_minutos_inicial = %s,\
                           end = %s, hora_minutos_final = %s,\
                           preco = %s\
                           WHERE id = %s;"

#Para a coluna utente da tabela Visita ficar junta à tabela
#Tarefa_Visita e para aparecerem os nomes dos grupos de tarefas em vez dos seus
#ids...
sql_tarefa_visita_visita_start = "SELECT Tarefa_Visita.*,\
                                  Visita.utente, Tarefa.tarifa, Visita.nome\
                                  AS grupo_tarefas_nome\
                                  FROM Tarefa_Visita\
                                  INNER JOIN Visita\
                                  ON Tarefa_Visita.visita=Visita.id\
                                  INNER JOIN Tarefa\
                                  ON Tarefa_Visita.title=Tarefa.nome\
                                  WHERE start = %s;"

#Para se juntar as colunas "tarifa" da tabela Tarefa e "nome" da tabela
#Categoria_tarefa à tabela Tarefa_Visita e para aparecerem os nomes dos
#grupos de tarefas em vez dos seus ids...
sql_tarefa_visita_tarefa_visita = "SELECT Tarefa_Visita.*,\
                                  Tarefa.tarifa, Tarefa.categoria,\
                                  Categoria_tarefa.nome AS categoria_nome,\
                                  Visita.nome AS grupo_tarefas_nome\
                                  FROM Tarefa_Visita\
                                  INNER JOIN Visita\
                                  ON Tarefa_Visita.visita=Visita.id\
                                  INNER JOIN Tarefa\
                                  ON Tarefa_Visita.title=Tarefa.nome\
                                  INNER JOIN Categoria_tarefa\
                                  ON Tarefa.categoria=Categoria_tarefa.id\
                                  WHERE visita = %s;"

#Para aquelas tarefas cuja tarifa é horária, eu pretendo que o seu preço seja
#introduzido na tabela Tarefa_Visita através da multiplicação do seu número de
#horas pelo seu preço original (o da tabela Tabela_precos, influenciado pelo
#escalão da pessoa que as criou)
sql_tarefa_visita_nome_escalao = "SELECT Tarefa_Visita.*, Tarefa.tarifa,\
                                 Tabela_precos.preco AS preco_original\
                                  FROM Tarefa_Visita\
                                  INNER JOIN Tarefa\
                                  ON Tarefa_Visita.title=Tarefa.nome\
                                  INNER JOIN Tabela_precos\
                                  ON Tarefa_Visita.title =\
                                  Tabela_precos.nome_tarefa\
                                  WHERE Tarefa_Visita.id = %s\
                                  AND Tabela_precos.nome_escalao = %s;"

## Comandos Tarefa
sql_nome_tarefa = "SELECT `nome` FROM Tarefa;"
sql_tarefa_nome = "SELECT * FROM Tarefa WHERE nome = %s;"

sql_tarefa_insert = "INSERT INTO `Tarefa` (`nome`, `categoria`,\
                    `tarifa`)\
                    VALUES (%s, %s, %s);"

#Para associar a coluna categoria à tabela Tarefa
sql_tarefa_cat_categoria_tarefa = "SELECT Tarefa.*, Categoria_tarefa.nome\
                                   AS categoria_nome\
                                   FROM Tarefa\
                                   INNER JOIN Categoria_tarefa\
                                   ON Tarefa.categoria = Categoria_tarefa.id;"

sql_tarefa_esc_preco = "SELECT Tarefa.*, Categoria_tarefa.nome\
                       AS categoria_nome, Tabela_precos.preco AS preco\
                       FROM Tarefa\
                       JOIN Categoria_tarefa\
                       ON Tarefa.categoria = Categoria_tarefa.id\
                       JOIN Tabela_precos\
                       ON Tarefa.nome = Tabela_precos.nome_tarefa\
                       WHERE Tabela_precos.nome_escalao = %s\
                       ORDER BY `nome` ASC;"

## Comandos Visita
sql_visita_id = "SELECT * FROM Visita WHERE id = %s;"
sql_visita_nome = "SELECT * FROM Visita WHERE nome = %s;"
sql_visita_utente = 'SELECT * FROM Visita WHERE utente = %s;'

sql_visita_insert = "INSERT INTO Visita (`nome`,`descricao`,`utente`)\
                                    VALUES (%s, %s, %s);"

sql_visita_update = "UPDATE Visita SET nome = %s, descricao = %s\
                      WHERE id = %s;"

## Comandos Categoria_tarefa
sql_categoria_tarefa = "SELECT * FROM Categoria_tarefa;"
sql_categoria_tarefa_nome = "SELECT * FROM Categoria_tarefa WHERE nome = %s;"

sql_categoria_tarefa_insert = "INSERT INTO `Categoria_tarefa` (`nome`)\
                              VALUES (%s);"

## Comandos Escalao_preco
sql_nome_escalao_preco = 'SELECT `nome` FROM Escalao_preco;'
sql_nome_nome_escalao_preco = 'SELECT `nome`, `nome` FROM Escalao_preco;'
sql_escalao_preco_nome = 'SELECT * FROM Escalao_preco WHERE nome = %s;'

sql_escalao_preco_insert = "INSERT INTO `Escalao_preco` (`nome`,`descricao`)\
                           VALUES (%s, %s);"

## Comandos Tabela_precos
sql_tabela_precos = 'SELECT `nome_tarefa`, `nome_escalao`, `preco`\
                     FROM Tabela_precos\
                     ORDER BY `nome_tarefa` ASC;'
sql_tabela_precos_tarefa_escalao = 'SELECT * FROM Tabela_precos\
                            WHERE nome_tarefa = %s AND nome_escalao = %s;'

sql_tabela_precos_insert = "INSERT INTO `Tabela_precos`\
                           (`nome_tarefa`, `nome_escalao`, `preco`)\
                           VALUES (%s, %s, %s);"

## Comandos Equipa
sql_equipa = 'SELECT `nome` FROM Equipa;'
sql_equipa_nome ="SELECT * FROM Equipa WHERE nome = %s;"

sql_equipa_insert = "INSERT INTO Equipa(`nome`) VALUES (%s);"

sql_equipa_delete = "DELETE FROM Equipa WHERE `nome` = %s;"

sql_equipa_update_nome = "UPDATE Equipa SET nome = %s WHERE nome = %s;"

## Comandos User_Equipa
sql_user_equipa_mon = "SELECT * FROM User_Equipa WHERE username = %s;"
sql_user_equipa_equipa = "SELECT username FROM User_Equipa WHERE equipa = %s;"

sql_user_equipa_insert = "INSERT INTO User_Equipa (`equipa`, `username`)\
                       VALUES (%s, %s);"

sql_user_equipa_delete = "DELETE FROM User_Equipa WHERE equipa = %s AND\
                         username = %s;"
sql_user_equipa_delete_equipa = "DELETE FROM User_Equipa WHERE `equipa` = %s;"

sql_user_equipa_update =\
                         "UPDATE User_Equipa SET equipa = %s WHERE equipa = %s;"

## Comandos User
sql_user = 'SELECT * FROM User;'
sql_username_mon = 'SELECT `username` FROM User WHERE nivel_de_acesso=%s;'
sql_user_username = "SELECT * FROM User WHERE username = %s;"
sql_user_telemovel ="SELECT * FROM User WHERE telemovel = %s;"
sql_user_email ="SELECT * FROM User WHERE email = %s;"
sql_user_id ="SELECT * FROM User WHERE id=%s;"

sql_user_insert = "INSERT INTO User(`username`,`nome`,`telemovel`,`email`,\
                  `categoria`, `nivel_de_acesso`,`password_hash`)\
                  VALUES (%s, %s, %s, %s, %s, %s, %s);"

sql_user_update = "UPDATE User SET telemovel = %s, email = %s,\
                      categoria = %s WHERE email = %s;"

## Comandos Categoria_user
sql_nome_nome_categoria_user = 'SELECT `nome`, `nome` FROM Categoria_user;'
sql_categoria_user_nome = 'SELECT * FROM Categoria_user WHERE nome = %s;'

sql_categoria_user_insert = "INSERT INTO Categoria_user (nome) VALUES (%s);"

## Comandos Utente
sql_utente = 'SELECT email, nome, telemovel, morada, esc_de_preco FROM Utente;'

sql_utente_email ="SELECT * FROM Utente WHERE email = %s;"
sql_utente_telemovel ="SELECT * FROM Utente WHERE telemovel = %s;"

sql_utente_insert = "INSERT INTO Utente(`nome`,`email`,`telemovel`,`morada`,\
                      `nome_a_contactar`,`num_a_contactar`,`med_fam_apoio`,\
                      `alergias`,`doencas`,`esc_de_preco`)\
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

sql_utente_update = "UPDATE Utente SET telemovel = %s, email = %s,\
                      morada = %s, nome_a_contactar = %s, num_a_contactar = %s,\
                      esc_de_preco = %s, med_fam_apoio = %s, alergias = %s,\
                      doencas = %s WHERE email = %s;"
sql_utente_comentarios = "UPDATE Utente SET comentarios = %s WHERE email = %s;"
