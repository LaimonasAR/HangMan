from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    PasswordField,
    FloatField,
    IntegerField,
    ValidationError,
    validators,
)
import requests


# import app
def check_user(form, email):
    user = requests.get("http://localhost:8000/api/v1/accounts/{email}")
    if user:
        raise ValidationError("This email is already in use. Please choose another.")


class RegistrationForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    surname = StringField("Surname", [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired(), check_user])
    password = PasswordField("Password", [validators.DataRequired()])
    password_validation = PasswordField(
        "Repeat password", [validators.EqualTo("password", "Passwords must match.")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField("Current password", [validators.DataRequired()])
    new_password = PasswordField("New Password", [validators.DataRequired()])
    new_password_validation = PasswordField(
        "Repeat new password",
        [validators.EqualTo("new_password", "Passwords must match.")],
    )
    submit = SubmitField("Change password")


class AccountUpdateForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    surname = StringField("Surname", [validators.DataRequired(), check_user])
    email = StringField("Email", [validators.DataRequired()])
    submit = SubmitField("Update")


def validate_one_letter(form, field):
    data = field.data
    if len(data) != 1 or not data.isalpha():
        raise ValidationError("Input must be a single letter.")


class LetterGuess(FlaskForm):
    letter = StringField("letter", [validators.DataRequired(), validate_one_letter])
    submit = SubmitField("Submit")


def validate_difficulty(form, field):
    data = field.data
    if int(data) < 5 or int(data) > 10:
        raise ValidationError("Input must be a number between 5 and 10.")


class Difficulty(FlaskForm):
    difficulty = IntegerField(
        "difficulty", [validators.DataRequired(), validators.NumberRange(min=5, max=10)]
    )
    play = SubmitField("Submit")
