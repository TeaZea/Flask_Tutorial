#blueprint should be imported and registered from the factory

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


#register form

#routes the url to the register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    #required variables needing to be input
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        #ensuring a username and/or password is given and can be posted
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        #validation succeeds
        if error is None:
            try:
                #replaces '?' placeholders with info given
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                #redirects users to login
                return redirect(url_for("auth.login"))
        
        #stores any error
        flash(error)

    return render_template('auth/register.html')


#login view

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        #checks user to see if it's in a table
        #fetches password to see if they're the same
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #if login is accepted, id is stored in session
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


