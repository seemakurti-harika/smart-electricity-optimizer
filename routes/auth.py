from flask import (
    render_template,
    request,
    redirect,
    session,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import app

from models.database import (
    get_db_connection
)


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = generate_password_hash(
            request.form['password']
        )

        conn = get_db_connection()

        existing_user = conn.execute(
            '''
            SELECT * FROM users
            WHERE email=?
            ''',
            (email,)
        ).fetchone()
        if existing_user:
            conn.close()

    return render_template(

        'signup.html',

        error="Email already exists"
    )
    conn.execute(
            '''
            INSERT INTO users
            (
                username,
                email,
                password
            )

            VALUES (?, ?, ?)
            ''',
            (
                username,
                email,
                password
            )
        )

    conn.commit()

    conn.close()

    return redirect('/login')

    return render_template('signup.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            '''
            SELECT * FROM users
            WHERE email=?
            ''',
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user['password'],
            password
        ):

            session['user_id'] = user['id']

            session['username'] = user['username']

            return redirect('/dashboard')

        else:
            return render_template(

        'login.html',

        error="Wrong password"
    )

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')