from flask import Blueprint


bp = Blueprint('vendor', __name__, template_folder='templates')

from app.vendor import routes