from flask import Flask, g, render_template, request 
import sqlite3

app = Flask(__name__)

def get_message_db():
    """
    Function: handles creating the database of messages.
    Check whether there is a database called message_db in the g attribute of the app. If not, then connect to that database, ensuring that the connection is an attribute of g.
    Check whether a table called messages exists in message_db, and create it if not. 
    Return: the connection g.message_db.
    """
    try:
        return g.message_db

    except: 

        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """

        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db
        
def insert_message():
    """
    Function: handle inserting a user message into the database of messages
    Extract the message and the handle from request.
    Using a cursor, insert the message into the message database.
    """
    message = request.form['message']
    handle = request.form['handle']
    
    conn = get_message_db()

    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ('{message}', '{handle}')
    """
    cursor = conn.cursor()
    cursor.execute(cmd)
    
    conn.commit()
    conn.close()

    return message, handle
    
@app.route('/submit/', methods=['POST', 'GET'])
def submit():

    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            message, handle = insert_message()
            return render_template('submit.html', submitted=True, message=message, handle=handle)
        except: 
            return render_template('submit.html', error=True)
            
def random_messages(n):
    """
    Function: return a collection of n random messages from the message_db, or fewer if necessary.
    """
    conn = get_message_db()
    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """

    cursor = conn.cursor()
    cursor.execute(cmd)

    result = cursor.fetchall()
    conn.close()

    return result
    
7), and then pass these messages as an argument to render_template().

@app.route('/view/')
def view(): 
    return render_template('view.html', messages=random_messages(7))
