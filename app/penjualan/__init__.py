from flask import Blueprint

bp = Blueprint('penjualan',__name__, template_folder='templates')

from app.penjualan import routes