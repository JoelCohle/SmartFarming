from flask import render_template, url_for, flash, redirect, request
from flaskapp.forms import LoginForm
from flaskapp.models import Admin
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import urllib.request, json

import os

Admins = [
    {
        'Email': 'admin@gmail.com',
        'password': 'admin'
    }
]

lighturl = "https://api.thingspeak.com/channels/1837535/fields/1.json?api_key=17B4FANCL381KHZE&results=30"
moistureurl = "https://api.thingspeak.com/channels/1837535/fields/2.json?api_key=17B4FANCL381KHZE&results=30"
tempurl = "https://api.thingspeak.com/channels/1837535/fields/3.json?api_key=17B4FANCL381KHZE&results=30"
humidityurl = "https://api.thingspeak.com/channels/1837535/fields/4.json?api_key=17B4FANCL381KHZE&results=30"
CO2url = "https://api.thingspeak.com/channels/1837535/fields/5.json?api_key=17B4FANCL381KHZE&results=30"
TVOCurl = "https://api.thingspeak.com/channels/1837535/fields/6.json?api_key=17B4FANCL381KHZE&results=30"
lightvalues = json.loads(urllib.request.urlopen(lighturl).read())
moisturevalues = json.loads(urllib.request.urlopen(moistureurl).read())
tempvalues = json.loads(urllib.request.urlopen(tempurl).read())
humidityvalues = json.loads(urllib.request.urlopen(humidityurl).read())
CO2values = json.loads(urllib.request.urlopen(CO2url).read())
TVOCvalues = json.loads(urllib.request.urlopen(TVOCurl).read())
ids = [val["entry_id"] for val in lightvalues["feeds"]]
light = [val["field1"] for val in lightvalues["feeds"]]
moisture = [val["field2"] for val in moisturevalues["feeds"]]
temperature = [val["field3"] for val in tempvalues["feeds"]]
humidity = [val["field4"] for val in humidityvalues["feeds"]]
co2 = [val["field5"] for val in CO2values["feeds"]]
tvoc = [val["field6"] for val in TVOCvalues["feeds"]]

@app.route('/')
@app.route("/home")
@login_required
def home():
    return render_template('home.html', ids=ids , lightvalues=light, moisturevalues=moisture, tempvalues=temperature, humidityvalues=humidity, CO2values=co2, TVOCvalues=tvoc)

@app.route('/graph')
@login_required
def graph():
    return render_template('graph.html', ids=ids , lightvalues=light, moisturevalues=moisture, tempvalues=temperature, humidityvalues=humidity, CO2values=co2, TVOCvalues=tvoc )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

    # trainee_1 = Trainee(name='John Doe', email='johndoe@gmail.com', designation='Jr Developer',date_of_joining=datetime(2022, 4, 20), training_start_date=datetime(2022, 4, 24), training_plannned_end_date=datetime(2022, 5, 24), training_actual_end_date=datetime(2022, 5, 24), project_allocated='ABC', team='XYZ', communication_rating=7, technical_rating=7, overall_rating=8, selected_role='Development', status='completed')