__author__ = 'Girish'

from flask import Blueprint

auth = Blueprint('auth', __name__)
from app.auth import routes
