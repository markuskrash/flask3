from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
import sqlite3
from flask_login import LoginManager


class PayForm(FlaskForm):
    number = StringField('Номер карты', validators=[DataRequired()])
    cvv = StringField('Код безопасности', validators=[DataRequired()])
    date = StringField('Дата окончания работы', validators=[DataRequired()])
    submit = SubmitField('Войти')
