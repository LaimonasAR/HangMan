import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    UserMixin,
    login_required,
)

from sqlalchemy import DateTime
from datetime import datetime
import secrets
import requests
from PIL import Image
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import forms
import models
from src import game
from flask_session import Session
from src.game import cor_lett, incor_lett, hidden_word_handling, Game
from src.rand_word import RandomWordGenerator

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'biudzetas.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "prisijungti"
# login_manager.login_message_category = 'info'
login_manager.login_message = "ka cia issidirbineji"


@login_manager.user_loader
def load_user(user_id: int):
    user_data = requests.get(f"http://localhost:8000/api/v1/accounts/account/{user_id}")
    if user_data.status_code == 200:
        user_dict = user_data.json()
        user = models.User(id=user_dict["id"], is_active=True)
        return user
    return None


@login_manager.unauthorized_handler
def guest_callback():
    return redirect(url_for("log_in"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_data = {
            "name": form.name.data,
            "surname": form.surname.data,
            "email": form.email.data,
            "password": pwd_hash,
        }
        response = requests.post(
            "http://localhost:8000/api/v1/accounts/", json=user_data
        )
        # flash("Account created successfully!", "success")
        # return redirect(url_for("log_in"))
        if response.status_code == 200:
            flash("Account created successfully!", "success")
            return redirect(url_for("log_in"))
        else:
            flash("Failed to create account. Email already in use.", "danger")
    return render_template("register.html", form=form)


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    form = forms.LoginForm()
    if form.validate_on_submit():
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/accounts/{form.email.data}"
        )

        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get("id")
            print(user_id)
            user_password = user_data.get("password")
            print(user_password)
            # user_status = user_data.get("is_active")
            user_status = True
            if user_data and bcrypt.check_password_hash(
                user_password, form.password.data
            ):
                user = models.User(id=user_id, is_active=user_status)
                login_user(user, remember=form.remember.data)
                return redirect(url_for("index"))
            else:
                flash("Login failed. Check email email and password", "danger")
    return render_template("log_in.html", title="Login", form=form)


@login_required
@app.route("/start", methods=["POST", "GET"])
def start():
    form = forms.Difficulty()
    if request.method == "POST":
        difficulty = request.form["difficulty"]
        word_to_guess = RandomWordGenerator(difficulty)
        word = word_to_guess.rand_word()
        session["word"] = word
        session["hidden_word"] = hidden_word_handling(
            session.get("word"), cor_letters=cor_lett
        )
        session["cor_lett"] = cor_lett
        session["incor_lett"] = incor_lett
        session["letters"] = difficulty
        session["message"] = ""
        # session["letters"] = 5
        # session["game_state"] = 0

        return redirect(url_for("play"))
    else:
        return render_template("start.html", form=form)


@login_required
@app.route("/play", methods=["GET", "POST"])
def play():
    form = forms.LetterGuess()

    if form.validate_on_submit():
        # if request.method == "POST":
        guess = form.letter.data
        # guess = request.form.get("letter")
        game = Game(
            session.get("word"),
            session.get("cor_lett"),
            session.get("incor_lett"),
            guess,
        )
        # response = game.play(session["word"], session["cor_lett"], session["incor_lett"], guess)
        response = game.play()
        print(response)
        if response["game_over"] == True and response["victory"] == True:
            return render_template("victory.html")
        elif response["game_over"] == True and response["victory"] == False:
            return render_template("defeat.html")
        else:
            session["message"] = response["message"]
            session["hidden_word"] = response["hidden_word"]
            session["cor_lett"] = response["cor_lett"]
            session["incor_lett"] = response["incor_lett"]
        return redirect(url_for("play"))
    hidden_word = session.get("hidden_word")
    cor_lett = session.get("cor_lett")
    incor_lett = session.get("incor_lett")
    # picture = "/static/img/%.jpg" % 1
    bad_tries = len(incor_lett)
    message = session.get("message")
    word = session.get("word")
    # remove these
    # game_over = response["game_over"]
    # victory = response["victory"]
    return render_template(
        "play.html",
        hidden_word=hidden_word,
        cor_lett=cor_lett,
        incor_lett=incor_lett,
        # picture=bad_tries,
        picture='images/0.jpg',
        message=message,
        word=word,
        # game_over=game_over,
        # victory=victory,
        form=form,
    )


@login_required
@app.route("/log_off")
def atsijungti():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/set/")
def set():
    session["key"] = "value"
    return "ok"


@app.route("/get/")
def get():
    return session.get("key", "not set")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


# @app.route("/game_old", methods=["GET", "POST"])
# @login_required
# def play_game():
#     # global game_id
#     try:
#         letter = request.form["letter"]
#         play_data = {"game_id": game_id, "guess_letter": letter}
#     except (NameError, KeyError):
#         return redirect(url_for("game"))

#     game_response = requests.post(
#         f"http://127.0.0.1:1337/api/v1/games/play/{game_id}", json=play_data
#     )
#     if game_response.status_code == 200:
#         game_data = game_response.json()
#         game_tries = game_data.get("game_tries")
#         game_display = game_data.get("game_display")
#         game_word_set = game_data.get("game_word_set")
#         game_status = game_data.get("status")

#     guesses = requests.get(
#         f"http://127.0.0.1:1337/api/v1/guesses/game_guesses/{game_id}"
#     )
#     if guesses.status_code == 200:
#         guesses_data = guesses.json()
#         user_guesses = [item.get("guess_letter") for item in guesses_data]

#     while game_status == "NEW":
#         return render_template(
#             "game.html",
#             game_display=game_display,
#             game_word_set=game_word_set,
#             game_draw="/static/img/hang%d.png" % game_tries,
#             game_tries=game_tries,
#             user_guesses=user_guesses,
#         )

#     return render_template(
#         "results.html",
#         game_status=game_status,
#         game_word=game_word,
#         game_display=game_display,
#         game_word_set=game_word_set,
#         game_draw="/static/img/hang%d.png" % game_tries,
#         game_tries=game_tries,
#         user_guesses=user_guesses,
#     )
