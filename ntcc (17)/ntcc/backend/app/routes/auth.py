from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose another.', 'warning')
            return redirect(url_for('auth.register'))

        cleaned_role = role.strip().lower()
        if cleaned_role == 'ngo':
            cleaned_role = 'recipient'

        if cleaned_role not in ['donor', 'recipient']:
            flash("Invalid role selected. Choose donor or recipient.", "danger")
            return redirect(url_for('auth.register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw, role=cleaned_role)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            role = user.role.strip().lower()
            if role == 'ngo':
                role = 'recipient'

            # ✅ Store using consistent session keys
            session['user_id'] = user.id
            session['user_role'] = role

            print(f"✅ Logged in as: {user.username} | Role: {role}")

            if role == 'donor':
                return redirect(url_for('donor.donor_dashboard'))
            elif role == 'recipient':
                return redirect(url_for('recipient.recipient_dashboard'))
            else:
                flash(f'Unknown role: {role}', 'danger')
                return redirect(url_for('auth.login'))

        flash('Invalid username or password.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
