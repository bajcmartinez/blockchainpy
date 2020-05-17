from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/', defaults={'page': 'index'})
def show(page):
    return "Home"