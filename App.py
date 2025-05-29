from flask import Flask, render_template, request, redirect, session
import sqlite3
import db
import config
import announcements
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex


app = Flask(__name__)
app.secret_key = config.secret_key


#render error page with error message and type
def errorpage(error_message, error_type):
    return render_template("errorpage.html", error_message=error_message, error_type=error_type)


# Check if CSRF token is valid
def check_csrf_token():
    if request.form["csrf_token"] != session["csrf_token"]:
        return errorpage("Invalid CSRF token", "Error while processing request")


# Render homepage with announcements
@app.route("/")
def index():
    all_announcements = announcements.get_announcements()
    return render_template("index.html", announcements=all_announcements)


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
            session["csrf_token"] = token_hex(16)
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
        salt = token_hex(16)    # Generate a random salt for password hashing

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


# Log out user
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")


# Render announcement creation page
@app.route("/new_announcement", methods=["GET", "POST"])
def new_announcement():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        check_csrf_token()
        title = request.form["title"]
        description = request.form["description"]
        download_link = request.form["download_link"]
        intented_price = request.form["intented_price"]
        age_restriction = request.form["age_restriction"]

        # Validate user input
        if not title or not description:
            return errorpage("All fields marked with * are required", "Error while creating announcement")
        if len(title) > 70:
            return errorpage("Title must be less than 70 characters", "Error while creating announcement")
        if len(description) > 1000:
            return errorpage("Description must be less than 1000 characters", "Error while creating announcement")
        if download_link:
            if not download_link.startswith("http"):
                return errorpage("Invalid download link", "Error while creating announcement")
        if intented_price:
            if not intented_price.isdigit():
                return errorpage("Price must be a number (0 for free), (currently supports only integers)", "Error while creating announcement")
        if age_restriction:
            if not age_restriction.isdigit():
                return errorpage("Age restriction must be a number", "Error while creating announcement")

        # Insert announcement into database
        announcements.add_announcement(session["user_id"], title, download_link, description, intented_price, age_restriction)
        return redirect("/")
    return render_template("new_announcement.html")


# Render announcement page
@app.route("/announcement/<int:announcement_id>")
def announcement(announcement_id):
    announcement = announcements.get_announcement(announcement_id)
    return render_template("announcement.html", announcement=announcement)


# Render announcement edit page
@app.route("/announcement/<int:announcement_id>/edit", methods=["GET", "POST"])
def edit_announcement(announcement_id):
    # Check if user is logged in
    if not session.get("username"):
        return redirect("/login")

    # Check if user is authorized to edit announcement
    announcement = announcements.get_announcement(announcement_id)
    if session["user_id"] != announcement["user_id"]:
        return errorpage("You are not authorized to edit this announcement", "Error while editing announcement")

    if request.method == "POST":
        check_csrf_token()
        if "confirm" in request.form:
            title = request.form["title"]
            description = request.form["description"]
            download_link = request.form["download_link"]
            intented_price = request.form["intented_price"]
            age_restriction = request.form["age_restriction"]

            # Validate user input
            if not title or not description:
                return errorpage("All fields marked with * are required", "Error while editing announcement")
            if len(title) > 100:
                return errorpage("Title must be less than 100 characters", "Error while editing announcement")
            if len(description) > 1000:
                return errorpage("Description must be less than 1000 characters", "Error while editing announcement")
            if download_link:
                if not download_link.startswith("http"):
                    return errorpage("Invalid download link", "Error while editing announcement")
            if intented_price:
                if not intented_price.isdigit():
                    return errorpage("Price must be a number (0 for free), (currently supports only integers)", "Error while editing announcement")
            if age_restriction:
                if not age_restriction.isdigit():
                    return errorpage("Age restriction must be a number", "Error while editing announcement")

            # Update announcement in database
            announcements.update_announcement(announcement_id, title, download_link, description, intented_price, age_restriction)
            return redirect("/announcement/" + str(announcement_id))
        return redirect("/announcement/" + str(announcement_id))
    return render_template("edit_announcement.html", announcement=announcement)


# Render announcement remove page
@app.route("/announcement/<int:announcement_id>/remove", methods=["GET", "POST"])
def remove_announcement(announcement_id):
    # Check if user is logged in
    if not session.get("username"):
        return redirect("/login")

    # Check if user is authorized to remove announcement
    announcement = announcements.get_announcement(announcement_id)
    if session["user_id"] != announcement["user_id"]:
        return errorpage("You are not authorized to remove this announcement", "Error while removing announcement")

    if request.method == "POST":
        check_csrf_token()
        if "remove" in request.form:
            announcements.remove_announcement(announcement_id)
            return redirect("/")
        return redirect("/announcement/" + str(announcement_id))
    return render_template("remove_announcement.html", announcement=announcement)




# Allows the app to run in IDE terminal in debug mode
if __name__ == "__main__":
    app.run(debug=True)
