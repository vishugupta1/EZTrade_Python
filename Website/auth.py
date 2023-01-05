from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import Stock
from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .MachineLearning import ImportData as ID
import pandas as pd
import datetime as dt
import sys

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        otp = request.form.get('otp')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully!', category='success')
                login_user(user, remember=True)
                data = ID.get_user_info(email, password, otp)
                for key,value in data:
                    new_stock = Stock(avgprice = value['average_buy_price'], quantity = value['quantity'])
                    db.session.add(new_stock)
                    db.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters.", category='error')
        elif len(lastName) < 2:
            flash("Last name must be greater than 1 characters.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash("Password must be atleast 7 characters.", category='error')
        else:
            new_user = User(email=email, firstName = firstName, lastName = lastName, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created.", category='success')
            return redirect(url_for('views.home'))
            # add user to database
    return render_template("sign_up.html", user=current_user)

@auth.route('/graph', methods=['GET'])
def graph():
    stocks_data = pd.DataFrame()
    stocks_data = ID.get_stock_data("IBM", dt.datetime(2008, 1, 1), dt.datetime(2009, 1, 1))
    data = [
        ("01-01-2020", 100),
        ("02-01-2020", 200),
        ("03-01-2020", 300),
        ("04-01-2020", 400),
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    print(stocks_data)
    values2 = stocks_data['Adj Close'].values.tolist()
    labels2 = []
    labels2 = stocks_data.index.tolist()
    print(values2)
    print(labels2)
    v = []
    for i in range(len(values2)):
        v.append(i)
    return render_template("graph.html", labels=v, values=values2, user=current_user)