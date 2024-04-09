import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, username, password FROM user WHERE username = ?', (username,)
        ).fetchone()
        print(user)
        print(user['password'])
        if user is None:
            error = 'Incorrect username.'
        elif not user['password'] == password:
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            user = db.execute(
                'SELECT id, name, email, username, about, location FROM user WHERE username = ?', (username,)
            ).fetchone()
            return list(user)
        return error

    return 