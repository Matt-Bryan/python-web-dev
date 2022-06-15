from hashlib import sha256
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            # Email too short
            flash('Email must be at least 4 characters', category='error')
        elif len(first_name) < 2:
            # First name too short
            flash('First name must be at least 2 characters in length', category='error')
        elif password1 != password2:
            # Password mismatch
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            # Password length requirement
            flash('Password must be at least 7 characters in length', category='error')
        else:
            # Add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html")