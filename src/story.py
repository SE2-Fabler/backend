from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from src.db import get_db

bp = Blueprint('story', __name__)

#helpers
def dbQueryFollowing(uid, db):
    query = 'SELECT DISTINCT u.id, name, email, username, about, location FROM follow f JOIN user u ON f.following_id = u.id WHERE' + (' f.user_id in ('+uid+')')
    following = db.execute(query).fetchall()
    out = []
    for row in following:
        out.append(list(row))
    return out
def dbAddFollowing(uid, fid, db):
    query = 'INSERT INTO follow (user_id, following_id) VALUES (' + uid + ', ' + fid +')'
    print(query)
    db.execute(query)
    db.commit()
    return True
def dbQueryCreations():
    return

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

@bp.route('/user/following', methods=('GET', 'POST'))
def getFollowing():
    db = get_db()
    if request.method == 'POST':
        uid = request.form['uid']
        fid = request.form['fid']
        print(uid)
        print(fid)
        dbAddFollowing(uid, fid, db)
        return "success"
    id = request.args.get('id')
    print(id)
    return dbQueryFollowing(id, db)