# import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    login_required,
)

import requests
import forms
import models
from flask_session import Session
from logic.game import cor_lett, incor_lett, hidden_word_handling, Game
from logic.rand_word import RandomWordGenerator

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "prisijungti"
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
            session["user_id"] = user_id
            user_password = user_data.get("password")
            user_status = True
            if user_data and bcrypt.check_password_hash(
                user_password, form.password.data
            ):
                user = models.User(id=user_id, is_active=user_status)
                pwd_hash = bcrypt.generate_password_hash(form.password.data).decode(
                    "utf-8"
                )
                session["password"] = pwd_hash
                session["email"] = form.email.data
                login_user(user, remember=form.remember.data)
                return redirect(url_for("index"))
            else:
                flash("Login failed. Check email and password", "danger")
    return render_template("log_in.html", title="Login", form=form)


@login_required
@app.route("/account", methods=["GET", "POST"])
def account():
    form = forms.AccountUpdateForm()
    if form.validate_on_submit():
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/accounts/{form.email.data}"
        )
        if response.status_code == 200:
            flash("Email already registered!", "danger")
            return redirect(url_for("account"))
        else:
            user_data = {
                "email": form.email.data,
                "name": form.name.data,
                "surname": form.surname.data,
            }
            user_id = session.get("user_id")
            response = requests.put(
                f"http://localhost:8000/api/v1/accounts/{user_id}", json=user_data
            )
            if response.status_code == 200:
                flash("Account updated successfully!", "success")
                return redirect(url_for("account"))
            else:
                flash("Changes failed. Check data", "danger")
    return render_template("account.html", form=form)


@login_required
@app.route("/pass_change", methods=["GET", "POST"])
def pass_change():
    form = forms.PasswordChangeForm()
    if form.validate_on_submit():
        email = session.get("email")
        password = session.get("password")
        print(password)
        new_pass = bcrypt.generate_password_hash(form.old_password.data).decode("utf-8")
        print(new_pass)
        response = requests.get(f"http://127.0.0.1:8000/api/v1/accounts/{email}")
        if response.status_code == 200 and bcrypt.check_password_hash(
            password, form.old_password.data
        ):
            hashed_pass = bcrypt.generate_password_hash(form.new_password.data).decode(
                "utf-8"
            )
            user_data = {
                "password": hashed_pass,
            }
            user_id = session.get("user_id")
            response2 = requests.put(
                f"http://localhost:8000/api/v1/accounts/password/{user_id}",
                json=user_data,
            )
            session["password"] = hashed_pass
            if response2.status_code == 200:
                flash(
                    "Password changed successfully! Please, log out and log in again!",
                    "success",
                )
                return redirect(url_for("pass_change"))
            else:
                flash("Changes failed. Check password", "danger")
        else:
            flash("Changes failed. Check password", "danger")
    return render_template("pass_change.html", form=form)


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
        return redirect(url_for("play"))
    else:
        user_id = session["user_id"]
        response = requests.get(f"http://127.0.0.1:8000/api/v1/games/{user_id}")
        response_data = response.json()
        user_data = []
        if response.status_code == 200:
            for game in response_data:
                if game["status"] is True:
                    status = "Won"
                else:
                    status = "Lost"
                game_data = {
                    "Word": game["word"],
                    "Correct letters": game["corrlett"],
                    "Incorrect letters": game["incorrlett"],
                    "Errors": game["error_count"],
                    "Won/lost": status,
                }
                user_data.append(game_data)

        return render_template("start.html", form=form, data=user_data)


@login_required
@app.route("/play", methods=["GET", "POST"])
def play():
    form = forms.LetterGuess()
    if form.validate_on_submit():
        guess = form.letter.data
        game = Game(
            session.get("word"),
            session.get("cor_lett"),
            session.get("incor_lett"),
            guess,
        )
        response = game.play()
        user_id = session.get("user_id")
        
        if response["game_over"] == True and response["victory"] == True:
            game_data = {
                "word": session.get("word"),
                "status": True,
                "corrlett": response["cor_lett"],
                "incorrlett": response["incor_lett"],
                "error_count": len(response["incor_lett"]),
            }
            response2 = requests.post(
                f"http://127.0.0.1:8000/api/v1/games/{user_id}", json=game_data
            )
            incor_lett = response["incor_lett"]
            bad_tries = len(incor_lett)
            picture="/images/%d.jpg" % bad_tries
            return render_template("victory.html", picture=picture)
        elif response["game_over"] == True and response["victory"] == False:
            game_data = {
                "word": session.get("word"),
                "status": False,
                "corrlett": response["cor_lett"],
                "incorrlett": response["incor_lett"],
                "error_count": len(response["incor_lett"]),
            }
            response2 = requests.post(
                f"http://127.0.0.1:8000/api/v1/games/{user_id}", json=game_data
            )
            return render_template("defeat.html")
        else:
            session["message"] = response["message"]
            session["hidden_word"] = response["hidden_word"]
            session["cor_lett"] = response["cor_lett"]
            session["incor_lett"] = response["incor_lett"]
        return redirect(url_for("play"))
    else:
        hidden_word = session.get("hidden_word")
        cor_lett = session.get("cor_lett")
        incor_lett = session.get("incor_lett")
        # picture = "/static/img/%.jpg" % 1
        bad_tries = len(incor_lett)
        message = session.get("message")
        word = session.get("word")
        return render_template(
            "play.html",
            hidden_word=hidden_word,
            cor_lett=cor_lett,
            incor_lett=incor_lett,
            # picture=bad_tries,
            # picture="images/0.jpg",
            picture="/images/%d.jpg" % bad_tries,
            message=message,
            word=word,
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
