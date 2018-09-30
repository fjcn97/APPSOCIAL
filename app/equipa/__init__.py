from flask import Blueprint

bp = Blueprint('equipa', __name__)

from app.equipa import routes
