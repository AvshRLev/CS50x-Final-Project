import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def response(messagedown, messageup):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("response.html", top=escape(messageup), bottom=escape(messagedown))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def merc(date):
    try:
        response = requests.get(f"https://mercuryretrogradeapi.com?date={date}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        a = response.json()
        return a["is_retrograde"]
    except (KeyError, TypeError, ValueError):
        return None

def apodlinks(date):
    """Look up links to APOD"""

    # Contact API
    try:
        date = date
        response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={date}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        pictures = response.json()
        return {
            "hdurl": pictures["hdurl"],
            "explanation": pictures["explanation"],
            "copyright": pictures["copyright"],
            "date": date
        }
    except (KeyError, TypeError, ValueError):
        return None


def getjoke():
    try:
        response = requests.get(f"https://sv443.net/jokeapi/v2/joke/Any?type=single")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        joke = response.json()
        return joke["joke"]
    except (KeyError, TypeError, ValueError):
        return None