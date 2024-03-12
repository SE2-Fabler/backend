from flask import Blueprint, jsonify, current_app
import requests
from models import User

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "Hello, World!"

@views.route('/make_request')
def make_request():
    response = requests.get('https://api.example.com/data')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

@views.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])