from flask import Flask, render_template, redirect, url_for, flash
import random
from models import db, User
from forms import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Example database
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('Email or username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/admin/tools/')
def admin_tools():
    return render_template('tool.html')

@app.route('/admin/users')
def admin_users():
    # Placeholder for user management functionality
    return "<h1>Manage Users</h1>"

@app.route('/admin/logs')
def admin_logs():
    # Placeholder for viewing logs
    return "<h1>View Logs</h1>"

@app.route('/admin/settings')
def admin_settings():
    # Placeholder for system settings
    return "<h1>System Settings</h1>"

@app.route('/admin/backup')
def admin_backup():
    # Placeholder for database backup functionality
    return "<h1>Database Backup</h1>"

@app.route('/admin/health')
def admin_health():
    # Placeholder for system health check
    return "<h1>System Health</h1>"

@app.route('/admin/clear-cache')
def admin_clear_cache():
    # Placeholder for clearing cache
    return "<h1>Clear Cache</h1>"

if __name__ == '__main__':
    app.run(debug=True)