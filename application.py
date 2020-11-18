import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, merc, response, apodlinks, getjoke

# Configure application
app = Flask(__name__)

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.route("/joke", methods=["GET", "POST"])
@login_required
def joke():
    """Get a random joke"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        joke = getjoke()
        user = session["user_id"]
        u_name = db.execute("SELECT username FROM users WHERE id = (:user)", user=user)
        db.execute("INSERT INTO transactions (username, time, joke) VALUES(:username, :time, :joke)",
                   username=u_name[0]["username"], time=datetime.datetime.now(), joke=joke[:10])
        return render_template("ajoke.html", joke=joke)

    # User reached route via GET
    else:
        return render_template("joke.html")


@app.route("/mercury", methods=["GET", "POST"])
@login_required
def mercury():
    """Check for Mercury retrograde"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = session["user_id"]
        u_name = db.execute("SELECT username FROM users WHERE id = (:user)", user=user)
        # Ensure a date to check was submitted
        if not request.form.get("date"):
            return apology("must provide a date to check", 403)
        formdate = datetime.datetime.strptime(request.form["date"], '%Y-%m-%d')
        today = datetime.datetime.now()
        # date_time_obj = datetime.datetime.strptime(formdate)
        boolian = merc(formdate)
        if boolian is True and request.form.get("date") == str(date.today()):
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("today", "mercury is in retrograde")
        elif boolian is False and request.form.get("date") == str(date.today()):
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("today", "mercury is not in retrograde")
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
        elif boolian is True and formdate > today:
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("on that day", "mercury will be in retrograde")
        elif boolian is False and formdate > today:
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("on that day", "mercury will not be in retrograde")
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
        elif boolian is True:
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("on that day", "mercury was in retrograde")
        else:
            db.execute("INSERT INTO transactions (username, time, mercstat, date_queried) VALUES(:username, :time, :mercstat, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), mercstat=boolian, date_queried=request.form.get("date"))
            return response("on that day", "mercury was not in retrograde")

    # User reached route via GET
    else:
        d2 = date.today()
        return render_template("mercury.html", today=d2)


@app.route("/apod", methods=["GET", "POST"])
@login_required
def apod():
    """ Show Astronomy Picture of the Day"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a date to check was submitted
        if not request.form.get("date"):
            return apology("must provide a date to check", 403)

        links = apodlinks(request.form.get("date"))
        if links == None:
            flash ("it appears that day had no picture or you have exceeded the amount of pictures for the time being try again later")
            user = session["user_id"]
            u_name = db.execute("SELECT username FROM users WHERE id = (:user)", user=user)
            db.execute("INSERT INTO transactions (username, time, apod_url, date_queried) VALUES(:username, :time, :apod_url, :date_queried)",
                       username=u_name[0]["username"], time=datetime.datetime.now(), apod_url="Did not retrieve a URL", date_queried=request.form.get("date"))
            return redirect("/apod")
        user = session["user_id"]
        u_name = db.execute("SELECT username FROM users WHERE id = (:user)", user=user)
        db.execute("INSERT INTO transactions (username, time, apod_url, date_queried) VALUES(:username, :time, :apod_url, :date_queried)",
                   username=u_name[0]["username"], time=datetime.datetime.now(), apod_url=links["hdurl"], date_queried=request.form.get("date"))
        return render_template("apod.html", links=links)


    # User reached route via GET
    else:
        d2 = date.today()
        return render_template("apod1.html", today=d2)


@app.route("/")
@login_required
def index():
        return render_template("index.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = session["user_id"]
    history = db.execute("SELECT * FROM transactions WHERE username = (SELECT username FROM users WHERE id = (:user)) ", user=user)
    transactions = []
    for row in history:
        time = row["time"]
        date_queried = row["date_queried"]
        apod_url = row["apod_url"]
        joke = row["joke"]
        mercstat = row["mercstat"]
        transactions.append({"time":time, "date_queried":date_queried, "apod_url":apod_url, "joke":joke, "mercstat":mercstat})
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure username does not exist in the database
        elif len(rows) == 1:
            return apology("Username taken, Please select another username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

         # Ensure password was resubmitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and password confirmation don't match")

        # Insert user into database with username and hashed password
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :has)",
                       username=request.form.get("username"),
                       has=generate_password_hash(request.form.get("password")))

            flash("User registered")
            return render_template("login.html")

    # User reached route via GET
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
