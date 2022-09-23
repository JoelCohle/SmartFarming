from flask import render_template, url_for, flash, redirect, request
from flaskapp.forms import LoginForm
from flaskapp.models import Admin
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from dateutil import parser
import urllib.request, json

import os

Admins = [
    {
        'Email': 'admin@gmail.com',
        'password': 'admin'
    }
]

lighturl = "https://api.thingspeak.com/channels/1837535/fields/1.json?api_key=17B4FANCL381KHZE&average=1&results=50"
moistureurl = "https://api.thingspeak.com/channels/1837535/fields/2.json?api_key=17B4FANCL381KHZE&average=1&results=50"
tempurl = "https://api.thingspeak.com/channels/1837535/fields/3.json?api_key=17B4FANCL381KHZE&average=1&results=50"
humidityurl = "https://api.thingspeak.com/channels/1837535/fields/4.json?api_key=17B4FANCL381KHZE&average=1&results=50"
CO2url = "https://api.thingspeak.com/channels/1837535/fields/5.json?api_key=17B4FANCL381KHZE&average=1&results=50"
TVOCurl = "https://api.thingspeak.com/channels/1837535/fields/6.json?api_key=17B4FANCL381KHZE&average=1&results=50"
lightvalues = json.loads(urllib.request.urlopen(lighturl).read())
moisturevalues = json.loads(urllib.request.urlopen(moistureurl).read())
tempvalues = json.loads(urllib.request.urlopen(tempurl).read())
humidityvalues = json.loads(urllib.request.urlopen(humidityurl).read())
CO2values = json.loads(urllib.request.urlopen(CO2url).read())
TVOCvalues = json.loads(urllib.request.urlopen(TVOCurl).read())

ids = [val+1 for val in range(len(lightvalues["feeds"]))]
# create a list of dates
dates = [parser.parse(val["created_at"]) for val in lightvalues["feeds"] if val["field1"] is not None]
light = [val["field1"] for val in lightvalues["feeds"] if val["field1"] is not None]
moisture = [val["field2"] for val in moisturevalues["feeds"] if val["field2"] is not None]
temperature = [val["field3"] for val in tempvalues["feeds"] if val["field3"] is not None]
humidity = [val["field4"] for val in humidityvalues["feeds"] if val["field4"] is not None ]
co2 = [val["field5"] for val in CO2values["feeds"] if val["field5"] is not None ]
tvoc = [val["field6"] for val in TVOCvalues["feeds"] if val["field6"] is not None]

@app.route('/')
@app.route("/home")
@login_required
def home():
    return render_template('home.html', ids=ids, dates=dates , lightvalues=light, moisturevalues=moisture, tempvalues=temperature, humidityvalues=humidity, CO2values=co2, TVOCvalues=tvoc)

@app.route('/graph')
@login_required
def graph():
    return render_template('graph.html', ids=ids, dates=dates , lightvalues=light, moisturevalues=moisture, tempvalues=temperature, humidityvalues=humidity, CO2values=co2, TVOCvalues=tvoc )


@app.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html', ids=ids , lightvalues=light, moisturevalues=moisture, tempvalues=temperature, humidityvalues=humidity, CO2values=co2, TVOCvalues=tvoc )


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