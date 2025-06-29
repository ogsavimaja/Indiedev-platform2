from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import db
import config
import announcements
import users
import markupsafe
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex


app = Flask(__name__)
app.secret_key = config.secret_key


# Render error page with error message and type
def errorpage(error_message, error_type):
    return render_template("errorpage.html", error_message=error_message, error_type=error_type)


# Check if user is logged in
def require_login():
    if not session.get("username"):
        return redirect("/login")


# Check if CSRF token is valid
def check_csrf_token():
    if request.form["csrf_token"] != session["csrf_token"]:
        return errorpage("Invalid CSRF token", "Error while processing request")


# Allows browser to see line breaks
@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


# Render homepage with announcements
@app.route("/")
def index():
    all_announcements = announcements.get_announcements()
    return render_template("index.html", announcements=all_announcements)


# Render user page
@app.route("/user/<int:user_id>")
def user(user_id):
    user_data = users.get_user(user_id)
    if not user_data:
        return errorpage("User not found", "Error while loading user")
    user_announcements = users.get_user_announcements(user_id)
    comments = users.get_user_comments(user_id)
    return render_template("userpage.html", user=user_data, announcements=user_announcements, comments=comments)


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
            flash("ERROR: All fields except email are required")
            return redirect("/register")
        if len(password) < 8:
            flash("ERROR: Password must be at least 8 characters long")
            return redirect("/register")
        if " " in password:
            flash("ERROR: Password cannot contain spaces")
            return redirect("/register")
        if len(username) < 3:
            flash("ERROR: Username must be at least 3 characters long")
            return redirect("/register")
        if " " in username:
            flash("ERROR: Username cannot contain spaces")
            return redirect("/register")
        if password != confirm_password:
            flash("ERROR: Passwords do not match")
            return redirect("/register")
        if email:
            if not "@" in email or not "." in email:
                flash("ERROR: Invalid email")
                return redirect("/register")

        # Check if username already exists, if not, create account
        try:
            sql_query = """INSERT INTO Users (username, salt, hashed_password, email)
                        VALUES (?, ?, ?, ?)"""
            db.execute(sql_query, [username, salt, generate_password_hash(password+salt), email])
        except sqlite3.IntegrityError:
            flash("ERROR: Username already exists")
            return redirect("/register")
        return redirect("/login")
    return render_template("register.html")


# Render login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            flash("ERROR: All fields are required")
            return redirect("/login")

        # Check if user exists
        sql_query = """SELECT id, username, hashed_password, salt
                       FROM Users
                       WHERE username = ?"""
        user_data = db.query(sql_query, [username])
        if not user_data:
            flash("ERROR: Invalid credentials")
            return redirect("/login")

        # Check if password is correct
        user_data = user_data[0]
        if check_password_hash(user_data["hashed_password"], (password + user_data["salt"])):
            session["username"] = user_data["username"]
            session["user_id"] = user_data["id"]
            session["csrf_token"] = token_hex(16)
            return redirect("/")
        flash("ERROR: Invalid credentials")
        return redirect("/login")
    return render_template("login.html")


# Log out user
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")


# Render search page
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        query = request.args.get("query")
        results = announcements.search_announcements(query) if query else None
        return render_template("search.html", query=query, results=results)
    return redirect("/")


# Render announcement page
@app.route("/announcement/<int:announcement_id>", methods=["GET", "POST"])
def announcement(announcement_id):
    if request.method == "POST":
        require_login()
        check_csrf_token()

        if not announcements.get_announcement(announcement_id):
            return errorpage("Announcement not found", "Error while loading announcement")

        comment = request.form["comment"].strip()
        if not comment:
            flash("ERROR: Comment cannot be empty")
            return redirect("/announcement/" + str(announcement_id))
        if len(comment) > 1000:
            flash("ERROR: Comment must be less than 1000 characters")
            return redirect("/announcement/" + str(announcement_id))
        announcements.add_comment(announcement_id, session["user_id"], comment)
        return redirect("/announcement/" + str(announcement_id))

    announcement = announcements.get_announcement(announcement_id)
    if not announcement:
        return errorpage("Announcement not found", "Error while loading announcement")

    result = announcements.get_one_announcement_classes(announcement_id)
    classes = result[0]
    lengths = result[1]
    comments = announcements.get_comments(announcement_id)
    return render_template("announcement.html", announcement=announcement, classes=classes, lengths=lengths, comments=comments)


# Render announcement creation page
@app.route("/new_announcement", methods=["GET", "POST"])
def new_announcement():
    require_login()
    result = announcements.get_announcement_classes()
    all_classes = result[0]
    class_types = result[1]
    if request.method == "POST":
        check_csrf_token()
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        download_link = request.form["download_link"]
        intented_price = request.form["intented_price"]
        age_restriction = request.form["age_restriction"]

        # Add classes into a list
        state = None
        classes = []
        for name in class_types.keys():
            result = request.form.getlist(name)
            if result != [""]:
                for value in result:
                    if value in all_classes[name]:
                        classes.append((name, value))
                        if name == "State":
                            state = True
                    else:
                        return errorpage("Invalid input", "Error while creating announcement")

        # Validate user input
        if not title or not description or not state:
            return errorpage("All fields marked with * are required", "Error while creating announcement")
        if len(title) > 70:
            return errorpage("Title must be less than 70 characters", "Error while creating announcement")
        if len(description) > 1000:
            return errorpage("Description must be less than 1000 characters", "Error while creating announcement")
        if download_link:
            if not download_link.startswith("http") or ":" not in download_link or "/" not in download_link or "." not in download_link:
                return errorpage("Invalid download link", "Error while creating announcement")
        if intented_price:
            if not intented_price.isdigit():
                return errorpage("Price must be a number (0 for free), (currently supports only integers)", "Error while creating announcement")
        if age_restriction:
            if not age_restriction.isdigit():
                return errorpage("Age restriction must be a number", "Error while creating announcement")

        # Insert announcement into database
        announcements.add_announcement(session["user_id"], title, download_link, description, intented_price, age_restriction, classes)
        return redirect("/")
    return render_template("new_announcement.html", classes=all_classes, class_types=class_types)


# Render announcement edit page
@app.route("/announcement/<int:announcement_id>/edit", methods=["GET", "POST"])
def edit_announcement(announcement_id):
    require_login()
    # Check if user is authorized to edit announcement
    announcement = announcements.get_announcement(announcement_id)
    if session["user_id"] != announcement["user_id"]:
        return errorpage("You are not authorized to edit this announcement", "Error while editing announcement")
    result = announcements.get_announcement_classes()
    all_classes = result[0]
    class_types = result[1]
    right_classes = announcements.get_one_announcement_classes(announcement_id)[0]
    if request.method == "POST":
        check_csrf_token()
        if "confirm" in request.form:
            title = request.form["title"].strip()
            description = request.form["description"].strip()
            download_link = request.form["download_link"]
            intented_price = request.form["intented_price"]
            age_restriction = request.form["age_restriction"]

            # Add classes into a list
            state = None
            classes = []
            for name in class_types.keys():
                result = request.form.getlist(name)
                if result != [""]:
                    for value in result:
                        if value in all_classes[name]:
                            classes.append((name, value))
                            if name == "State":
                                state = True
                        else:
                            return errorpage("Invalid input", "Error while creating announcement")

            # Validate user input
            if not title or not description or not state:
                return errorpage("All fields marked with * are required", "Error while editing announcement")
            if len(title) > 70:
                return errorpage("Title must be less than 70 characters", "Error while editing announcement")
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
            announcements.update_announcement(announcement_id, title, download_link, description, intented_price, age_restriction, classes)
            return redirect("/announcement/" + str(announcement_id))
        return redirect("/announcement/" + str(announcement_id))
    return render_template("edit_announcement.html", announcement=announcement, classes=all_classes, class_types=class_types, right_classes=right_classes)


# Render announcement remove page
@app.route("/announcement/<int:announcement_id>/remove", methods=["GET", "POST"])
def remove_announcement(announcement_id):
    # Check if announcement excist, user is logged in and authorized to remove announcement
    announcement = announcements.get_announcement(announcement_id)
    if not announcement:
        return errorpage("Announcement not found", "Error while removing announcement")
    require_login()
    if session["user_id"] != announcement["user_id"]:
        return errorpage("You are not authorized to remove this announcement", "Error while removing announcement")

    if request.method == "POST":
        check_csrf_token()
        if "remove" in request.form:
            announcements.remove_announcement(announcement_id)
            return redirect("/")
        return redirect("/announcement/" + str(announcement_id))
    return render_template("remove_announcement.html", announcement=announcement)


# Render comment edit page
@app.route("/announcement/<int:announcement_id>/comment/<int:comment_id>/edit", methods=["GET", "POST"])
def edit_comment(announcement_id, comment_id):
    # Check if comment excist, user is logged in and is authorized to edit comment
    comment = announcements.get_comment(comment_id)
    if not comment:
        return errorpage("Comment not found", "Error while editing comment")
    require_login()
    if session["user_id"] != comment["user_id"]:
        return errorpage("You are not authorized to edit this comment", "Error while editing comment")
    announcement = announcements.get_announcement(announcement_id)

    if request.method == "POST":
        check_csrf_token()
        if "confirm" in request.form:
            new_comment = request.form["comment"].strip()
            if not new_comment:
                return errorpage("Comment cannot be empty", "Error while editing comment")
            if len(new_comment) > 1000:
                return errorpage("Comment must be less than 1000 characters", "Error while editing comment")
            announcements.update_comment(comment_id, new_comment)
            return redirect("/announcement/" + str(announcement_id))
        return redirect("/announcement/" + str(announcement_id))
    return render_template("edit_comment.html", comment=comment, announcement=announcement)


# Render comment remove page
@app.route("/announcement/<int:announcement_id>/comment/<int:comment_id>/remove", methods=["GET", "POST"])
def remove_comment(announcement_id, comment_id):
    # Check if comment excist, user is logged in and is authorized to remove comment
    comment = announcements.get_comment(comment_id)
    if not comment:
        return errorpage("Comment not found", "Error while removing comment")
    require_login()
    if session["user_id"] != comment["user_id"]:
        return errorpage("You are not authorized to remove this comment", "Error while removing comment")
    announcement = announcements.get_announcement(announcement_id)

    if request.method == "POST":
        check_csrf_token()
        if "remove" in request.form:
            announcements.remove_comment(comment_id)
            return redirect("/announcement/" + str(announcement_id))
        return redirect("/announcement/" + str(announcement_id))
    return render_template("remove_comment.html", comment=comment, announcement=announcement)



# Allows the app to run in IDE terminal in debug mode
if __name__ == "__main__":
    app.run(debug=True)
