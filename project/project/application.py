import os
import pytz

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for
from flask.helpers import get_flashed_messages
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv("../doc.env")


# Configure application
app = Flask(__name__)

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Creating the upload folder
upload_folder = "static/uploads/"
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = upload_folder

# max. size of the file.
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

# configuring the allowed extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', "pdf"])


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///notes.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If the mathod is post chacking all the rquirement is fullfil.
    if request.method == "POST":
        username = request.form.get("username")
        users = db.execute("SELECT username, email FROM users")
        print(users)
        if not username:
            return apology("must provide username.", 400)

        elif username:
            for user in users:
                if username in user["username"]:
                    return apology("username is not available.", 400)

        password = request.form.get("password")
        if not password:
            return apology("must provide password.", 400)

        if not request.form.get("confirmation"):
            return apology("must provide confirmation.", 400)

        email = request.form.get("email")
        if not email:
            return apology("must provid email.", 403)
        elif email:
            for user in users:
                if email in user["email"]:
                    return apology("Entered email is already registered.", 400)

        # Checking if the the password and confirmation password matches.
        if password != request.form.get("confirmation"):
            return apology("password and confirmation password should match", 400)

        # Adding the new user into the users table
        db.execute("INSERT INTO users(username, hash, email) VALUES(?,?, ?)", username, generate_password_hash(password), email)

        # Simply redirecting to the login page.
        return redirect("/login")

    else:

        # Otherwise simply get the registration page.
        return render_template("register.html",)


# User account Delete.
@app.route("/delete_account", methods=['GET', 'POST'])
@login_required
def delete_Account():
    if request.method == "POST":
        Id = session["user_id"]
        row = db.execute("SELECT * FROM users WHERE id = ?", Id)
        username = row[0]['username']

        # checking for password
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        if username == request.form.get("username"):

            # Deleting the information of logged in user from database i.e from users table.
            db.execute("DELETE FROM users WHERE username = ?", request.form.get("username"))
            return redirect("/logout")

    return render_template("delete_account.html")


# Reset password page
@app.route("/reset", methods=["POST", "GET"])
def reset_password():

    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return apology("must provide email", 403)

        row = db.execute("SELECT * FROM users WHERE email =?", email)

        # Cheking that email id should be registered.
        if len(row) != 1:
            return apology("Must provide registered email address")

        # Sending a mail to registered email id with change password link.
        name = row[0]['username']
        message = Message("Muggle Notes: Reset password", recipients=[email])
        message.html = render_template("mail.html", name=name)
        mail.send(message)
        return redirect("/login")

    return render_template("reset.html")


# Change password link
@app.route("/new_password", methods=["POST", "GET"])
def new_password():
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get('username')
        if not password or not confirmation:
            return apology("must provide password or/and confirmation password.", 403)

        # Checking if the the password and confirmation password matches.
        if password != request.form.get("confirmation"):
            return apology("password and confirmation password should match", 403)

        # Updating the password for the user in users table in the database.
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(password), username)
        return redirect("/login")

    return render_template("new_password.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# function for upload files.
@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_image():
    if request.method == "POST":

        # Getting the list of files selected by the user.
        files = request.files.getlist('files[]')
        for file in files:
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)

            # Checking if the selecting files are allowed for uploading.
            if file and allowed_file(file.filename):

                # Getting the same file name as selected by the user
                filename = secure_filename(file.filename)

                # getting the file name and file extension.
                first = filename.rsplit('.', 1)[0]
                second = filename.rsplit('.', 1)[1]

                # after uploading selecting all the files from uploads table in database.
                uploads = db.execute("SELECT filename FROM uploads WHERE id=? AND filename LIKE ?", session["user_id"], first+"%")

                # counting the number of times uploaded files are alredy exists in uploaded files.
                count = len(uploads)
                print(uploads)
                if count != 0:
                    filename = first+"_("+str(count)+")."+second
                db.execute("INSERT INTO uploads(id, filename, date) VALUES(?,?,?)", session["user_id"], filename, datetime.now())

                # Saving the file in upload folder.
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File(s) successfully uploaded and stored in MY files below')
                return render_template('uploads.html')
            else:
                # or else if uploaded files are not allowed then just return the url.
                flash('Allowed file types are - png, jpg, jpeg, gif, pdf')
                return redirect(request.url)
    return render_template('uploads.html')


# This function will show the uploaded files in a tabular form in My files.
@app.route("/show_uploads")
@login_required
def show():
    uploads = db.execute("SELECT * FROM uploads WHERE id = ? ORDER BY(date) DESC", session["user_id"])
    return render_template("showUploads.html", uploads=uploads)


# share button for ever page.
@app.route("/share_buttons")
def share():
    return render_template("share.html")


# for upload icons
@app.route("/upload_files")
def files():
    return render_template("uploads.html")


# funtion for adding a new note.
@app.route("/add_new")
@login_required
def add_new():
    Id = session["user_id"]
    row = db.execute("SELECT * FROM users WHERE id = ?", Id)
    return render_template("add_new_note.html", username=row[0]["username"])

