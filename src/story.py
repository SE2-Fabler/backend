from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from src.db import get_db

bp = Blueprint('story', __name__)

@bp.route('/story')
def getStory():
    db = get_db()
    print(request.query_string)
    query = 'SELECT s.id, title, name, created, genre, body, bookmarks, bookmarked FROM story s JOIN user u ON s.author_id = u.id'
    if(len(request.query_string)):
        title = request.args.get('title')
        id = request.args.get('id')
        print(id)
        query += ' WHERE'
        if (len(id)):
            query += (' s.id in ('+id+')')
    stories = db.execute(query).fetchall()
    out = []
    for row in stories:
        out.append(list(row))
    return out