from flask import render_template, redirect, url_for, flash, request
from . import auth
from app import db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, SignInForm, RequestResetForm, ResetPasswordForm
from app.utils import send_reset_email

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already exists. Please sign in.', 'danger')
            return redirect(url_for('auth.sign_in'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            email=form.email.data, 
            password=hashed_password,
            role_A='Patient'  # Default role assignment
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('auth.sign_in'))

    return render_template('sign_up.html', form=form)

@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check email and password or sign up if you do not have an account.', 'danger')

    return render_template('sign_in.html', form=form)

@auth.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.sign_in'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('auth.sign_in'))
        else:
            flash('No account found with that email.', 'danger')
    return render_template('request_reset.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.sign_in'))
    return render_template('reset_password.html', form=form, token=token)
