from flask import (
    render_template,
    request,
    redirect,
    session,
    
)

from app import app

from models.database import (
    get_db_connection
)


# ADD REMINDER
@app.route('/add_reminder', methods=['GET', 'POST'])
def add_reminder():

    if 'user_id' not in session:

        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']

        reminder_time = request.form['reminder_time']

        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO reminders
            (
                user_id,
                title,
                reminder_time
            )

            VALUES (?, ?, ?)
            ''',
            (
                session['user_id'],
                title,
                reminder_time
            )
        )
         
        conn.commit()

        conn.close()

        return redirect('/dashboard')

    return render_template('add_reminder.html')
# EDIT REMINDER
@app.route('/edit_reminder/<int:id>', methods=['GET', 'POST'])
def edit_reminder(id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    reminder = conn.execute(
        '''
        SELECT * FROM reminders
        WHERE id=? AND user_id=?
        ''',
        (id, session['user_id'])
    ).fetchone()

    if request.method == 'POST':

        title = request.form['title']

        reminder_time = request.form['reminder_time']

        conn.execute(
            '''
            UPDATE reminders
            SET title=?,
                reminder_time=?
            WHERE id=? AND user_id=?
            ''',
            (
                title,
                reminder_time,
                id,
                session['user_id']
            )
        )

        conn.commit()

        conn.close()

        return redirect('/dashboard')

    conn.close()

    return render_template(
        'edit_reminder.html',
        reminder=reminder
    )


# DELETE REMINDER
@app.route('/delete_reminder/<int:id>')
def delete_reminder(id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    conn.execute(
        '''
        DELETE FROM reminders
        WHERE id=? AND user_id=?
        ''',
        (id, session['user_id'])
    )

    conn.commit()

    conn.close()

    return redirect('/dashboard')