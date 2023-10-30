from flask import Blueprint

from . import db
from .models import Stores, Items

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "Nyahallo world~!"