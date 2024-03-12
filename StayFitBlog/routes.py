# routes.py
from flask import Blueprint, render_template
from models import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Access db here
    return render_template('index.html')
