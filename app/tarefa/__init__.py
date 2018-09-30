from flask import Blueprint

bp = Blueprint('tarefa', __name__)

from app.tarefa import routes
