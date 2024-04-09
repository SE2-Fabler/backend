from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
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
def dbQueryBookmarks(uid, db):
    query = 'SELECT DISTINCT s.id, title, name, author_id, created, genre, body, bookmarks, bookmarked, private FROM bookmark m JOIN story s ON m.book_id = s.id JOIN user u ON s.author_id = u.id WHERE' + (' m.user_id in ('+uid+')')
    bookmarks = db.execute(query).fetchall()
    out = []
    for row in bookmarks:
        out.append(list(row))
    return out
def dbAddBookmark(uid, bid, db):
    query = 'INSERT INTO bookmark (user_id, book_id) VALUES (' + uid + ', ' + bid +')'
    print(query)
    db.execute(query)
    db.commit()
    return True

@bp.route('/story', methods=('GET', 'PUT', 'DELETE'))
def getStory():
    db = get_db()
    print(request.query_string)
    if request.method == 'PUT':
        prev = False
        query = 'UPDATE story SET'
        id = request.form.get('id')
        title = request.form.get('title')
        if (not title is None):
            query += ' title = \'' + title + '\''
            prev = True
        private = request.form.get('private')
        if (not private is None):
            if (prev): query += ','
            query += ' private = \'' + private + '\''
            prev = True
        query += ' WHERE id = ' + id
        print(query)
        db.execute(query)
        db.commit()
        return "success"
    elif request.method == 'DELETE':
        id = request.args.get('id')
        query = 'DELETE FROM story WHERE id = ' + id
        db.execute(query)
        db.commit()
        query = 'DELETE FROM bookmark WHERE book_id = ' + id
        db.execute(query)
        db.commit()
        return "success"
    query = 'SELECT s.id, title, name, author_id, created, genre, body, bookmarks, bookmarked, private FROM story s JOIN user u ON s.author_id = u.id'
    if(len(request.query_string)):
        title = request.args.get('title')
        id = request.args.get('id')
        author_id = request.args.get('author_id')
        print(id)
        print(title)
        print(author_id)
        query += ' WHERE'
        if (id):
            query += (' s.id in ('+id+')')
        elif (title):
            query += (' LOWER(title) LIKE \'%'+title+'%\'')
        elif (author_id):
            query += (' author_id in ('+author_id+')')
        print(query)
    stories = db.execute(query).fetchall()
    out = []
    for row in stories:
        out.append(list(row))
    return out

@bp.route('/story/bookmark', methods=('GET', 'POST', 'DELETE'))
def getBookmark():
    db = get_db()
    if request.method == 'POST':
        uid = request.form['uid']
        bid = request.form['bid']
        print(uid)
        print(bid)
        dbAddBookmark(uid, bid, db)
        return "success"
    elif request.method == 'DELETE':
        print('delete bookmark')
        id = request.args.get('id')
        uid = session.get('user_id')
        print(session.get('user_id'))
        if (not session.get('user_id') is None):
            query = 'DELETE FROM bookmark WHERE user_id = ' + str(uid) + ' AND book_id = ' + id
            print(query)
            db.execute(query)
            db.commit()
            return 'success'
        return 'not logged in'
    id = request.args.get('id')
    print(id)
    return dbQueryBookmarks(id, db)

@bp.route('/user', methods=('GET', 'PUT'))
def getUser():
    db = get_db()
    print(request.query_string)
    if request.method == 'PUT':
        print('put')
        prev = False
        query = 'UPDATE user SET'
        id = request.form.get('id')
        name = request.form.get('name')
        if (not name is None):
            query += ' name = \'' + name + '\''
            prev = True
        username = request.form.get('username')
        if (not username is None):
            if (prev): query += ','
            query += ' username = \'' + username + '\''
            prev = True
        password = request.form.get('password')
        if (not password is None):
            if (prev): query += ','
            query += ' password = \'' + password + '\''
            prev = True
        email = request.form.get('email')
        if (not email is None):
            if (prev): query += ','
            query += ' email = \'' + email+ '\''
            prev = True
        about = request.form.get('about')
        if (not about is None):
            if (prev): query += ','
            query += ' about = \'' + about + '\''
            prev = True
        location = request.form.get('location')
        if (not location is None):
            if (prev): query += ','
            query += ' location = \'' + location+ '\''
            prev = True
        query += ' WHERE id = ' + id
        print(query)
        db.execute(query)
        db.commit()
        return "success"
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

@bp.route('/user/following', methods=('GET', 'POST', 'DELETE'))
def getFollowing():
    db = get_db()
    if request.method == 'POST':
        uid = request.form['uid']
        fid = request.form['fid']
        print(uid)
        print(fid)
        dbAddFollowing(uid, fid, db)
        return "success"
    elif request.method == 'DELETE':
        print('delete follow')
        id = request.args.get('id')
        uid = session.get('user_id')
        print(session.get('user_id'))
        if (not session.get('user_id') is None):
            query = 'DELETE FROM follow WHERE user_id = ' + str(uid) + ' AND following_id = ' + id
            print(query)
            db.execute(query)
            db.commit()
            return 'success'
        return 'not logged in'
    id = request.args.get('id')
    print(id)
    return dbQueryFollowing(id, db)