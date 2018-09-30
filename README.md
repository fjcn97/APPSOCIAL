# PROJETOS PROFISSIONAIS

### Ainda poderei vir a melhorar mais a aplicação.
### NÃO é garantido que funcione em todos os sistemas operativos, navegadores, etc.

#### APPSOCIAL:

##### 	Serve para ajudar pessoas muito jovens ou idosas a realizarem determinados tipos de tarefas.
##### 	Testei-a a maior parte do tempo no Chromium 68 (do Zorin OS) e, no fim, no Firefox 62.

#####   Para efetuar operações na BD, usei o driver PYMYSQL. Todos os comandos sql e todos os ficheiros que criam as tabelas encontram-se na pasta sql, dentro da pasta app. Nela, encontra-se o ficheiro que permite inserir um administrador.
#####   Como nunca tinha programado com Flask, segui este tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Para executar a aplicação (em Ubuntu), pela primeira vez:
	1 - No terminal, ir para a pasta APPSOCIAL.
	2 - Criar ambiente virtual com: python3 -m venv venv (aplicação desenvolvida em Python 3.7)
	3 - Executá-lo com: source venv/bin/activate
	4 - Atualizar o pip3 com: pip3 install --upgrade pip
	5 - Instalar pacotes com: pip3 install -r requirements.txt (ver pacotes instalados com pip3 freeze)
	6 - Iniciá-la com: python3 APPSOCIAL.py *
    
Para executar a aplicação (em Windows 10), pela primeira vez:
    1 - Executar o terminal como administrador e ir para a pasta APPSOCIAL.
	2 - Criar ambiente virtual com: python -m venv venv (aplicação desenvolvida em Python 3.7) (Se com python3 ele não gerar o ficheiro activate.bat, usar só python)
    3 - Instalar pymysql no sistema com: pip install pymysql
	4 - Executar o ambiente com: venv\Scripts\activate
	5 - Atualizar o pip3 com: python -m pip install --upgrade pip
	6 - Instalar pacotes com: pip3 install -r requirements_windows.txt (ver pacotes instalados com pip3 freeze)
    7 - Seguir as instruções em: https://weasyprint.readthedocs.io/en/latest/install.html#windows . Se der erro, seguir as instruções em https://weasyprint.readthedocs.io/en/latest/install.html#gtk-64-bit-installer, fechar o terminal e executá-lo em modo admin. Se der erro, seguir as instruções em https://weasyprint.readthedocs.io/en/latest/install.html#step-5-run-weasyprint, fechar o terminal e executá-lo em modo admin.
	8 - Iniciá-la com: python APPSOCIAL.py *
    
* NÃO esquecer: Nas vezes seguintes, basta ir para a pasta APPSOCIAL, executar source venv/bin/activate ou venv\Scripts\activate e, depois, python[3] APPSOCIAL.py .

Para criar um requirements.txt: pip3 freeze > requirements.txt

Informações importantes:
	Várias páginas têm no URL "/user_id", porque, nestas, aparece uma caixa que contém a equipa e a categoria do monitor. Se entrarem com uma conta de monitor, vê-la-ão.
	Não cheguei a eliminar todo o "hardcode".
	Nalguns templates, tenho "if user == current_user". Isto serve para o caso de ter iniciado sessão, por exemplo, na conta do user 1 e, no link, mudar o 1 para 2. Assim, ao efetuar esta mudança, não poderei adicionar, alterar ou remover "coisas" estando na conta do user 2. Só poderei selecionar. Caso queira efetuar alguma daquelas operações, devo iniciar sessão na conta do user 2.
	Na pasta static, encontram-se todos os estilos no ficheiro style.css .
	Na pasta static, encontra-se a pasta dist. Nesta, encontram-se os ficheiros relativos ao funcionamento do mapa.
	Quando se clica num ponto do mapa, aparecem as suas coordenadas. Não fiz a funcionalidade de lê-las e de inseri-las na BD.
	As funções "load_naoseique" encontram-se no ficheiro models.py.

Lista de "coisas" que assumi ao longo do desenvolvimento da aplicação (não estão todas...):
	O administrador pode adicionar outros administradores, monitores ou utentes. Os monitores não podem adicionar ninguém. A categoria refere-se aos administradores e aos monitores. A interface não difere entre tipos de administradores ou tipos de monitores. Os utentes não mexem na aplicação!
	Os monitores não podem gerir equipas. Só consultar a equipa onde pertencem.
	Um administrador não pode passar a ser monitor, nem vice-versa!
	Considerei que todos os administradores e monitores têm emails diferentes. Considerei que todos os administradores e monitores têm telemóveis diferentes (não importante).
	Considerei que todos os utentes têm emails diferentes. Considerei que todos os utentes têm telemóveis diferentes (não importante).
	Considerei que a pessoa a contactar é um familiar próximo.
	Os utilizadores das equipas são só monitores. Nas equipas podem estar monitores de categorias diferentes!
	Não é obrigatório que os administradores, ao adicionarem um novo monitor, o associem a uma equipa no momento. Um monitor pode pertencer a mais do que uma equipa!
	O botão "Abrir histórico de tarefas" contém o histórico de tarefas do utente. Não contém as tarefas que ainda estão para serem efetuadas.
    Considerei o escalão "Sem escalão". Os escalões são lidos da tabela Escalao_preco - não são criados novos no momento da criação dos utentes. Na tabela de preços, ver-se-ão preços fixos para cada tarefa-base (exemplo: "Ida a consulta/ tratamento médico"), para cada escalão.
	Considerei que a duração esperada difere entre cada tarefa-base do mesmo grupo, para, depois, aparecer o seu tempo total, através da soma de todas as durações esperadas.
	Independentemente do escalão, há tarefas-base cuja tarifa é sempre fixa e outras cuja tarifa é sempre horária.
	Assim, se todas as tarefas de um mesmo grupo tiverem tarifa fixa, o preço total é a soma dos seus preços (não esquecendo que cada um destes varia consoante o escalão do utente).
