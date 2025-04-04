from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime
from wtforms import  PasswordField, BooleanField
from flask_moment import Moment
from datetime import datetime
from dotenv import load_dotenv
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name???', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LogingPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])
    password = PasswordField('Password', validators=[
    DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Investor Name:', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z]* ', 0,
                                                                                         'Usernames must have only letters')])
    username = StringField('User ID: ', validators=[DataRequired(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Usernames must have only letters, numbers, dots or '
    'underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])
    password = PasswordField('Password', validators=[
    DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ParkingReservationForm(FlaskForm):
    license_plate = StringField('License Plate', validators=[DataRequired(), Length(1, 20)])
    parking_spot = StringField('Parking Spot', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('Reserve Spot')

@app.route('/')
def index():
    return render_template('index.html',
                            current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    name="This is the name:  "+name
    return render_template('user.html', name=name)

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LogingPassForm()
    if form.validate_on_submit():
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you new investor please register using your email!')
        session['email'] = form.email.data
        return redirect(url_for('login'))
    flash('Welcome!')
    return render_template('login.html',form = form, name = session.get('name'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/robochat/')
def depsek():
    return render_template('dsindex.html')

@app.route('/ask', methods=['POST'])
def ask_deepseek():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "Empty query"}), 400

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",  # Confirm correct model name
            "messages": [{"role": "user", "content": user_query}]
        }

        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # Raise HTTP errors

        result = response.json()
        return jsonify({"answer": result['choices'][0]['message']['content']})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except KeyError:
        return jsonify({"error": "Unexpected API response format"}), 500

@app.route('/parking/')
def parking():
    # Generate parking spots for each lot
    lot1 = [{"spot": f"Lot 1 - Spot {i}", "available": random.choice([True, False])} for i in range(1, 21)]  # 20 spaces
    lot2 = [{"spot": f"Lot 2 - Spot {i}", "available": random.choice([True, False])} for i in range(1, 31)]  # 30 spaces
    lot3 = [{"spot": f"Lot 3 - Spot {i}", "available": random.choice([True, False])} for i in range(1, 41)]  # 40 spaces
    lot4 = [{"spot": f"Lot 4 - Spot {i}", "available": random.choice([True, False])} for i in range(1, 41)]  # 40 spaces

    # Pass the data to the template
    return render_template('parking.html', lot1=lot1, lot2=lot2, lot3=lot3, lot4=lot4)

@app.route('/reserve/', methods=['GET', 'POST'])
def reserve():
    form = ParkingReservationForm()
    if form.validate_on_submit():
        # Logic to reserve a parking spot (e.g., save to database)
        flash(f"Spot {form.parking_spot.data} reserved for {form.license_plate.data}!")
        return redirect(url_for('parking'))
    return render_template('reserve.html', form=form)

@app.route('/admin/tools/')
def admin_tools():
    return render_template('tool.html')

@app.route('/admin/users')
def admin_users():
    # Example user data (replace with database query in production)
    users = [
        {"id": 1, "username": "admin", "email": "admin@example.com", "role": "Admin"},
        {"id": 2, "username": "johndoe", "email": "johndoe@example.com", "role": "User"},
        {"id": 3, "username": "janedoe", "email": "janedoe@example.com", "role": "User"},
    ]
    return render_template('users.html', users=users)

@app.route('/admin/logs')
def admin_logs():
    # Example log data (replace with actual log retrieval in production)
    logs = [
        {"timestamp": "2025-04-04 10:00:00", "level": "INFO", "message": "User admin logged in."},
        {"timestamp": "2025-04-04 10:05:00", "level": "WARNING", "message": "Failed login attempt for user johndoe."},
        {"timestamp": "2025-04-04 10:10:00", "level": "ERROR", "message": "Database connection timeout."},
    ]
    return render_template('logs.html', logs=logs)

@app.route('/admin/settings', methods=['GET'])
def admin_settings():
    return render_template('settings.html')

@app.route('/admin/settings/update', methods=['POST'])
def update_settings():
    app_name = request.form.get('appName')
    admin_email = request.form.get('adminEmail')
    maintenance_mode = request.form.get('maintenanceMode')

    # Example: Save settings (replace with actual database or config file logic)
    print(f"Updated Settings: App Name={app_name}, Admin Email={admin_email}, Maintenance Mode={maintenance_mode}")

    flash('Settings updated successfully!', 'success')
    return redirect(url_for('admin_settings'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



