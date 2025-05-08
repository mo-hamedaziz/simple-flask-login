from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for('main.signup'))

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Signup successful! Please log in.")
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.welcome'))
        else:
            flash("Invalid username/email or password")
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', user=current_user)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))