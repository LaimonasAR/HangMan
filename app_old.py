import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    UserMixin,
    login_required,
)
import requests

from sqlalchemy import DateTime
from datetime import datetime
import secrets
from PIL import Image
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from fastapi import Depends, FastAPI, Request, Response, Form, HTTPException
from router.router import api_router
from database.db import engine, Base
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from endpoints import accounts_api
import httpx


# from forms.forms import RegistracijosForma, PrisijungimoForma, PaskyrosAtnaujinimoForma, IrasasForm


# class ManoModelView(ModelView):
#     def is_accessible(self):
#         return (
#             current_user.is_authenticated and current_user.el_pastas == "asdf@gmail.com"
#         )


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, "static/profilio_nuotraukos", picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "biudzetas.db"
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "prisijungti"
# login_manager.login_message_category = 'info'
login_manager.login_message = "ka cia issidirbineji"


# class Vartotojas(UserMixin):
# #    __tablename__ = "vartotojas"
#     response = requests.get("http://localhost:8000/api/v1/accounts/")

#     if response.status_code == 200:
#         data = response.json()  # Assuming the response contains JSON data

#     id = db.Column(db.Integer, primary_key=True)
#     vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
#     el_pastas = db.Column(
#         "El. pašto adresas", db.String(120), unique=True, nullable=False
#     )
#     nuotrauka = db.Column(db.String(20), nullable=False, default="default.jpg")
#     slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)


# class Irasas(db.Model):
#     __tablename__ = "irasas"
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column("Data", DateTime, default=datetime.now())
#     pajamos = db.Column("Pajamos", db.Boolean)
#     suma = db.Column("Vardas", db.Integer)
#     vartotojas_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
#     vartotojas = db.relationship("Vartotojas", lazy=True)


# admin = Admin(app)
# # admin.add_view(ModelView(Irasas, db.session))
# admin.add_view(ManoModelView(Vartotojas, db.session))


import forms.forms


@login_manager.user_loader
def load_user(user_id: str) -> Vartotojas:
    return Vartotojas.query.get(int(user_id))


@app.route("/registruotis", methods=["GET", "POST"])
def registruotis():
    # db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(
            form.slaptazodis.data
        ).decode("utf-8")
        vartotojas = {
            "name": form.vardas.data,
            "email": form.el_pastas.data,
            "password": koduotas_slaptazodis,
        }
        # db.session.add(vartotojas)
        # db.session.commit()
        url = "http://localhost:8000/api/v1/accounts/"
        response = requests.post(url, json=vartotojas)
        flash("Sėkmingai prisiregistravote! Galite prisijungti", "success")
        return redirect(url_for("index"))
    return render_template("registruotis.html", title="Register", form=form)


@app.route("/prisijungti", methods=["GET", "POST"])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash(
                "Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį", "danger"
            )
    return render_template("prisijungti.html", title="Prisijungti", form=form)


@app.route("/atsijungti")
def atsijungti():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/irasai")
# @login_required
# def irasai():
#     return render_template('irasai.html', title='Įrašai')


@app.route("/paskyra", methods=["GET", "POST"])
@login_required
def paskyra():
    form = forms.forms.PaskyrosAtnaujinimoForma()

    if form.validate_on_submit():
        if form.nuotrauka.data:
            nuotrauka = save_picture(form.nuotrauka.data)
            current_user.nuotrauka = nuotrauka
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash("Tavo paskyra atnaujinta!", "success")
        return redirect(url_for("paskyra"))
    elif request.method == "GET":
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    nuotrauka = url_for(
        "static", filename="profilio_nuotraukos/" + current_user.nuotrauka
    )
    return render_template(
        "paskyra.html", title="Account", form=form, nuotrauka=nuotrauka
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
