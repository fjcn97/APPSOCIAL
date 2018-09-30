from app import create_app

app = create_app()

#Para os campos horas e minutos do template edit_tarefa_visita.html
def split_pelos_2pontos(string):
    return string.split(':')

if __name__ == "__main__":
    app.jinja_env.filters['split_pelos_2pontos'] = split_pelos_2pontos
    app.run(debug=True)
