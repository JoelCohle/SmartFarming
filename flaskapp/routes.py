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

healthylighturl = "https://api.thingspeak.com/channels/1837535/fields/1.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
healthymoistureurl = "https://api.thingspeak.com/channels/1837535/fields/2.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
healthytempurl = "https://api.thingspeak.com/channels/1837535/fields/3.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
healthyhumidityurl = "https://api.thingspeak.com/channels/1837535/fields/4.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
healthyCO2url = "https://api.thingspeak.com/channels/1837535/fields/5.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
healthyTVOCurl = "https://api.thingspeak.com/channels/1837535/fields/6.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-22%2014:00:00&end=2022-09-23%2010:00:00&round=2"
deceasedlighturl = "https://api.thingspeak.com/channels/1837535/fields/1.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
deceasedmoistureurl = "https://api.thingspeak.com/channels/1837535/fields/2.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
deceasedtempurl = "https://api.thingspeak.com/channels/1837535/fields/3.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
deceasedhumidityurl = "https://api.thingspeak.com/channels/1837535/fields/4.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
deceasedCO2url = "https://api.thingspeak.com/channels/1837535/fields/5.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
deceasedTVOCurl = "https://api.thingspeak.com/channels/1837535/fields/6.json?api_key=17B4FANCL381KHZE&average=30&days=5&start=2022-09-23%2012:00:00&end=2022-09-24%2010:00:00&round=2"
healthylightvalues = json.loads(urllib.request.urlopen(healthylighturl).read())
healthymoisturevalues = json.loads(urllib.request.urlopen(healthymoistureurl).read())
healthytempvalues = json.loads(urllib.request.urlopen(healthytempurl).read())
healthyhumidityvalues = json.loads(urllib.request.urlopen(healthyhumidityurl).read())
healthyCO2values = json.loads(urllib.request.urlopen(healthyCO2url).read())
healthyTVOCvalues = json.loads(urllib.request.urlopen(healthyTVOCurl).read())
deceasedlightvalues = json.loads(urllib.request.urlopen(deceasedlighturl).read())
deceasedmoisturevalues = json.loads(urllib.request.urlopen(deceasedmoistureurl).read())
deceasedtempvalues = json.loads(urllib.request.urlopen(deceasedtempurl).read())
deceasedhumidityvalues = json.loads(urllib.request.urlopen(deceasedhumidityurl).read())
deceasedCO2values = json.loads(urllib.request.urlopen(deceasedCO2url).read())
deceasedTVOCvalues = json.loads(urllib.request.urlopen(deceasedTVOCurl).read())

ids = [val+1 for val in range(len(healthylightvalues["feeds"]))]
# create a list of dates
healthydates = [parser.parse(val["created_at"]) for val in healthylightvalues["feeds"] if val["field1"] is not None]
healthylight = [val["field1"] for val in healthylightvalues["feeds"] if val["field1"] is not None]
healthymoisture = [val["field2"] for val in healthymoisturevalues["feeds"] if val["field2"] is not None]
healthytemperature = [val["field3"] for val in healthytempvalues["feeds"] if val["field3"] is not None]
healthyhumidity = [val["field4"] for val in healthyhumidityvalues["feeds"] if val["field4"] is not None ]
healthyco2 = [val["field5"] for val in healthyCO2values["feeds"] if val["field5"] is not None ]
healthytvoc = [val["field6"] for val in healthyTVOCvalues["feeds"] if val["field6"] is not None]
deceaseddates = [parser.parse(val["created_at"]) for val in deceasedlightvalues["feeds"] if val["field1"] is not None]
deceasedlight = [val["field1"] for val in deceasedlightvalues["feeds"] if val["field1"] is not None]
deceasedmoisture = [val["field2"] for val in deceasedmoisturevalues["feeds"] if val["field2"] is not None]
deceasedtemperature = [val["field3"] for val in deceasedtempvalues["feeds"] if val["field3"] is not None]
deceasedhumidity = [val["field4"] for val in deceasedhumidityvalues["feeds"] if val["field4"] is not None ]
deceasedco2 = [val["field5"] for val in deceasedCO2values["feeds"] if val["field5"] is not None ]
deceasedtvoc = [val["field6"] for val in deceasedTVOCvalues["feeds"] if val["field6"] is not None]

@app.route('/')
@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/table")
@login_required
def table():
    return render_template('table.html', ids=ids, dates=healthydates, lightvalues=healthylight, moisturevalues=healthymoisture, tempvalues=healthytemperature, humidityvalues=healthyhumidity, CO2values=healthyco2, TVOCvalues=healthytvoc)

@app.route('/graph')
@login_required
def graph():
    return render_template('graph.html', ids=ids, dates=healthydates, healthylightvalues=healthylight, deceasedlightvalues=deceasedlight, moisturevalues=healthymoisture, tempvalues=healthytemperature, humidityvalues=healthyhumidity, healthyCO2values=healthyco2, deceasedCO2values=deceasedco2, healthyTVOCvalues=healthytvoc, deceasedTVOCvalues=deceasedtvoc )


@app.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html', ids=ids , healthymoisturevalues=healthymoisture, deceasedmoisturevalues=deceasedmoisture, healthytempvalues=healthytemperature, deceasedtempvalues=deceasedtemperature, healthyhumidityvalues=healthyhumidity, deceasedhumidityvalues=deceasedhumidity)


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