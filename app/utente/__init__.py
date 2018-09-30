from flask import Blueprint

bp = Blueprint('utente', __name__)

from app.utente import routes
