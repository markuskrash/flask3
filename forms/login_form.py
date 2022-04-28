from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
import sqlite3
from flask_login import LoginManager


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')
