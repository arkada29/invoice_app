from flask import Blueprint

bp = Blueprint('barang', __name__, template_folder='templates')

from app.barang import routes