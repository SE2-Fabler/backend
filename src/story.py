from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from src.db import get_db

bp = Blueprint('story', __name__)

@bp.route('/story')
def getStory():
    db = get_db()
    print(request.query_string)
    query = 'SELECT s.id, title, name, author_id, created, genre, body, bookmarks, bookmarked FROM story s JOIN user u ON s.author_id = u.id'
    if(len(request.query_string)):
        title = request.args.get('title')
        id = request.args.get('id')
        print(id)
        print(title)
        query += ' WHERE'
        if (id):
            query += (' s.id in ('+id+')')
        elif (title):
            query += (' LOWER(title) LIKE \'%'+title+'%\'')
        print(query)
    stories = db.execute(query).fetchall()
    out = []
    for row in stories:
        out.append(list(row))
    return out

@bp.route('/user')
def getUser():
    db = get_db()
    print(request.query_string)
    query = 'SELECT id, name, email, username, about, location FROM user'
    if (len(request.query_string)):
        username = request.args.get('query')
        print(username)
        query += ' WHERE'
        if (username):
            query += (' LOWER(name) LIKE \'%'+username+'%\'')
            query += (' OR LOWER(username) LIKE \'%'+username+'%\'')
    users = db.execute(query).fetchall()
    out = []
    for row in users:
        out.append(list(row))
    return out