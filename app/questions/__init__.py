__author__ = 'Girish'
from flask import Blueprint
questions =Blueprint("questions",__name__)
from app.questions import routes
