from flask import Blueprint

bp = Blueprint('unit', __name__, template_folder='templates')

from app.unit import routes