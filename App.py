from flask import Flask, render_template, request, redirect, session
import sqlite3
import db
import config
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex


app = Flask(__name__)
app.secret_key = config.secret_key

#render error page with error message and type
def errorpage(error_message, error_type):
    return render_template("errorpage.html", error_message=error_message, error_type=error_type)

@app.route("/")
def index():
    return render_template("index.html")

# Render login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return errorpage("All fields are required", "Error while logging in")

        # Check if user exists
        sql_query = """SELECT id, username, hashed_password, salt
                       FROM Users
                       WHERE username = ?"""
        user_data = db.query(sql_query, [username])
        if not user_data:
            return errorpage("Invalid Credentials", "Error while logging in")

        # Check if password is correct
        user_data = user_data[0]
        if check_password_hash(user_data["hashed_password"], (password + user_data["salt"])):
            session["username"] = user_data["username"]
            session["user_id"] = user_data["id"]
            return redirect("/")
        return errorpage("Invalid Credentials", "Error while logging in")
    return render_template("login.html")

# Render registeration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        salt = token_hex(10)

        # Validate user input
        if not username or not password or not confirm_password:
            return errorpage("All fields except email are required", "Error while creating account")
        if len(password) < 8:
            return errorpage("Password must be at least 8 characters long", "Error while creating account")
        if len(username) < 3:
            return errorpage("Username must be at least 3 characters long", "Error while creating account")
        if password != confirm_password:
            return errorpage("Passwords do not match", "Error while creating account")
        if email:
            if not "@" in email or not "." in email:
                return errorpage("Invalid email", "Error while creating account")


        # Check if username already exists, if not, create account
        try:
            sql_query = """INSERT INTO Users (username, salt, hashed_password, email)
                        VALUES (?, ?, ?, ?)"""
            db.execute(sql_query, [username, salt, generate_password_hash(password+salt), email])
        except sqlite3.IntegrityError:
            return errorpage("Username already exists", "Error while creating account")
        return render_template("account_created.html")
    return render_template("register.html")



# Allows the app to run on IDE in debug mode
if __name__ == "__main__":
    app.run(debug=True)
