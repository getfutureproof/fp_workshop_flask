from flask import Flask, g, render_template, request, session
from db import get_db
import hashlib

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def hash_function(input):
    return hashlib.sha256(input.encode()).hexdigest()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # TODO: See if _database is removed from 'g' here
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/new", methods=['GET', 'POST'])
def new_trees():
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        cursor.execute(
            "INSERT INTO trees (id, name, species) VALUES (?, ?, ?);",
            (2, name, species)
        )
        db.commit()

    cursor.execute("SELECT * from trees")
    trees = cursor.fetchall()

    return render_template("new.html", trees=trees)


@app.route("/register", methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # Check whether the passwords match
        if password1 != password2:
            message = "Passwords do not match"
            return render_template("register.html", message=message)

        # Check whether anyone with this username has already registered
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username, ))
        count = cursor.fetchone()[0]
        if count > 0:
            message = "User with username already exists"
            return render_template("register.html", message=message)

        hashed_password = hash_function(password1)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        message = "Successfully registered"
    return render_template("register.html", message=message)


@app.route("/login", methods=['GET', 'POST'])
def login():
    message = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username, ))
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.execute("SELECT password FROM users WHERE username=?", (username, ))
            password_in_database = cursor.fetchone()[0]
            if hash_function(password) == password_in_database:
                session['authenticated'] = True
                message = "You have successfully logged in"
            else:
                message = "Incorrect password"
        else:
            message = "No user with that username"

    return render_template("login.html", message=message)


@app.route("/private")
def private():
    if not "authenticated" in session:
        return "You are not allowed here"
    
    return "Welcome to my secret lair"


@app.route("/logout")
def logout():
    del session['authenticated']
    return "Thank you for visiting"
