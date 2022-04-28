from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login_form import LoginForm
from forms.pay_form import PayForm
from forms.registr_form import RegisterForm
from data import db_session
from data.basket import User_bt
from data.users import User
from data.antibacterial_menu import Antibacterial
from data.antiviral_menu import Antiviral
from data.hygiene_menu import Hygiene
from data.mental_menu import Mental
from data.immune_menu import Immune
from data.painkiller_menu import Painkiller
import csv

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_menu():
    return render_template("main_menu.html")


@app.route('/login', methods=['POST', 'GET'])
def login_menu():
    form = LoginForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('login_menu.html',
                                   error_email="Пользователя с такой почтой нет",
                                   form=form)
        if not user.check_password(form.password.data):
            return render_template('login_menu.html',
                                   error_password="Неверный пароль",
                                   form=form)
        login_user(user, remember=True)
        return redirect("/")
    return render_template('login_menu.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# @app.route('/pay', methods=['POST', 'GET'])
# def pay_menu():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         print(1)
#         number_card = form.Card_number.data
#         card_expiration_date = form.Expiration_date_card.data
#         cvv_card = form.Card_cvv.data
#         error_number_card = None
#         error_card_expiration_date = None
#         error_cvv_card = None
#         if len(number_card) != 16 and not number_card.isdigit():
#             error_number_card = 'Неправильный формат ввода.'
#         if len(cvv_card) != 3 and not cvv_card.isdigit():
#             error_cvv_card = 'Неправильный формат ввода.'
#         if len(card_expiration_date) != 5 and not '/' in card_expiration_date:
#             error_card_expiration_date = 'Непривльный формат ввода.'
#         else:
#             x = error_card_expiration_date.split('/')
#             # if len(x[0]) != 2 and not x[0]


@app.route('/registration', methods=['POST', 'GET'])
def registr_menu():
    form = RegisterForm()
    if form.validate_on_submit():
        print(1)
        db_sess = db_session.create_session()
        error_name = None
        error_email = None
        if db_sess.query(User).filter(User.name == form.name.data).first():
            error_name = 'Пользователь с таким именем уже есть'
        if db_sess.query(User).filter(User.email == form.email.data).first():
            error_email = "Пользователь с такой почтой уже есть"
        if error_email or error_name:
            return render_template('registr_menu.html', title='Регистрация',
                                   form=form, error_name=error_name,
                                   error_email=error_email)
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('registr_menu.html', form=form)


def add_drugs(class_name, csv_name):
    db_sess = db_session.create_session()
    with open(f"csv/{csv_name}", encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for i in reader:
            if not db_sess.query(class_name).filter(class_name.title == i['title']).first():
                drugs = class_name(
                    title=i['title'],
                    price=i['price'],
                )
                db_sess.add(drugs)
                db_sess.commit()


@app.route('/antibacterial')
def antibacterial_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Antibacterial)
    return render_template("antibacterial_menu.html", menu=menu)


@app.route('/antiviral')
def antiviral_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Antiviral)
    return render_template("antiviral_menu.html", menu=menu)


@app.route('/hygiene')
def hygiene_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Hygiene)
    return render_template("hygiene_menu.html", menu=menu)


@app.route('/immune')
def immune_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Immune)
    return render_template("immune_menu.html", menu=menu)


@app.route('/mental')
def mental_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Mental)
    return render_template("mental_menu.html", menu=menu)


@app.route('/painkiller')
def painkiller_assortiment():
    db_sess = db_session.create_session()
    menu = db_sess.query(Painkiller)
    return render_template("painkiller_menu.html", menu=menu)


@app.route('/basket')
def basket():
    db_sess = db_session.create_session()
    if current_user:
        menu = db_sess.query(User_bt).filter(User_bt.email == current_user.email)
    else:
        menu = db_sess.query(User_bt).filter(User_bt.email == '')
    sum = 0
    for i in menu:
        sum += i.count * i.price
    return render_template("basket_menu.html", menu=menu, sum=sum)


@app.route('/add_basket/<string:categ>/<string:drug>_<int:price>', methods=['GET', 'POST'])
@login_required
def add_basket(categ, drug, price):
    db_sess = db_session.create_session()
    print(categ)
    user = User_bt(
        email=current_user.email,
        drug=drug,
        price=price
    )
    if db_sess.query(User_bt).filter(User_bt.drug == drug).first():
        db_sess.query(User_bt).filter(User_bt.drug == drug).first().count += 1
    else:
        user.count = 1
        db_sess.add(user)
    db_sess.commit()

    return redirect(f'/{categ}')


@app.route('/pay_basket', methods=['POST', 'GET'])
def pay_menu():
    form = PayForm()
    db_sess = db_session.create_session()
    menu = db_sess.query(User_bt).filter(User_bt.email == current_user.email)
    sum = 0
    for i in menu:
        sum += i.count * i.price
    if form.is_submitted():
        users = db_sess.query(User_bt)
        for user in users:
            db_sess.delete(user)
        db_sess.commit()
        return redirect("/success_pay")
    if sum == 0:
        return redirect("/basket")
    return render_template('pay_menu.html', title='Покупка', form=form, sum=sum)


@app.route('/success_pay', methods=['POST', 'GET'])
def success_menu():
    return render_template('success_menu.html', title='Успешная оплата')


@app.route('/del_basket/<string:categ>/<string:drug>', methods=['GET', 'POST'])
@login_required
def del_basket(categ, drug):
    db_sess = db_session.create_session()
    user = db_sess.query(User_bt).filter(User_bt.drug == drug and
                                         User_bt.email == current_user).first()
    db_sess.delete(user)
    db_sess.commit()
    return redirect(f'/{categ}')


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    add_drugs(Antibacterial, 'assortiment_antibact.csv')
    add_drugs(Antiviral, 'assortiment_antiviral.csv')
    add_drugs(Hygiene, 'assortiment_hygiene.csv')
    add_drugs(Immune, 'assortiment_immune.csv')
    add_drugs(Mental, 'assortiment_mental.csv')
    add_drugs(Painkiller, 'assortiment_painkiller.csv')
    app.run('127.0.0.1', 8080)
