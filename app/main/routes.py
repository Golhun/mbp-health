from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from . import main
from app import db, bcrypt
from app.forms import ProfileForm, BloodPressureForm, HeartRateForm, CholesterolForm, GlucoseForm
from app.models import User, BloodPressure, Cholesterol, HeartRate, Glucose
from werkzeug.security import generate_password_hash
from PIL import Image
from datetime import datetime, timedelta
from flask import jsonify


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/summary')
@login_required
def summary():
    form = BloodPressureForm()
    bp_data = BloodPressure.query.filter_by(user_id=current_user.id).all()
    cholesterol_data = Cholesterol.query.filter_by(user_id=current_user.id).all()
    heart_rate_data = HeartRate.query.filter_by(user_id=current_user.id).all()
    glucose_data = Glucose.query.filter_by(user_id=current_user.id).all()
    return render_template('summary_content.html', form=form, bp_data=bp_data, cholesterol_data=cholesterol_data, heart_rate_data=heart_rate_data, glucose_data=glucose_data)


@main.route('/profile')
@login_required
def profile():
    form = ProfileForm(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,  # Include email
        date_of_birth=current_user.date_of_birth,
        height=current_user.height,
        weight=current_user.weight,
        medications=current_user.medications,
        allergies=current_user.allergies
    )
    return render_template('profile_content.html', user=current_user, form=form)

@main.route('/explore')
@login_required
def explore_content():
    return render_template('explore_content.html')

@main.route('/dashboard')
@login_required
def dashboard():
    form = ProfileForm()
    return render_template('dashboard.html', form=form)

@main.route('/edit_profile_page')
@login_required
def edit_profile_page():
    form = ProfileForm(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,  # Include email
        date_of_birth=current_user.date_of_birth,
        height=current_user.height,
        weight=current_user.weight,
        medications=current_user.medications,
        allergies=current_user.allergies
    )
    return render_template('edit_profile_page.html', form=form)

@main.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update profile fields
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data  # Update email
        current_user.date_of_birth = form.date_of_birth.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.medications = form.medications.data
        current_user.allergies = form.allergies.data
        
        # Handle password update
        if form.old_password.data and form.new_password.data and form.confirm_password.data:
            if bcrypt.check_password_hash(current_user.password, form.old_password.data):
                if form.new_password.data == form.confirm_password.data:
                    current_user.password = generate_password_hash(form.new_password.data)
                    flash('Your password has been updated successfully!', 'success')
                else:
                    flash('New password and confirm password do not match.', 'danger')
                    return redirect(url_for('main.edit_profile_page'))
            else:
                flash('Old password is incorrect.', 'danger')
                return redirect(url_for('main.edit_profile_page'))

        # Commit changes to the database
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Error updating your profile. Please check your inputs.', 'danger')
        return redirect(url_for('main.edit_profile_page'))

@main.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.edit_profile_page'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.edit_profile_page'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static/uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Compress and save the image
        image = Image.open(file_path)
        image = image.resize((400, 400), Image.LANCZOS)
        image.save(file_path, optimize=True, quality=85)

        current_user.profile_picture = filename
        db.session.commit()
        flash('Profile picture updated!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid file format', 'danger')
        return redirect(url_for('main.edit_profile_page'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@main.route('/blood_pressure', methods=['GET', 'POST'])
@login_required
def blood_pressure():
    form = BloodPressureForm()
    if form.validate_on_submit():
        bp = BloodPressure(
            user_id=current_user.id,
            systolic=form.systolic.data,
            diastolic=form.diastolic.data
        )
        db.session.add(bp)
        db.session.commit()
        return jsonify(success=True)
    elif request.method == 'POST':
        return jsonify(success=False, errors=form.errors)

    bp_data = BloodPressure.query.filter_by(user_id=current_user.id).all()
    bp_data_formatted = [{'timestamp': bp.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'systolic': bp.systolic, 'diastolic': bp.diastolic} for bp in bp_data]
    return render_template('blood_pressure.html', form=form, bp_data=bp_data_formatted)

@main.route('/blood_pressure_data')
@login_required
def blood_pressure_data():
    view = request.args.get('view', 'day')
    
    if view == 'day':
        # Fetch daily data
        bp_data = BloodPressure.query.filter_by(user_id=current_user.id).all()
    elif view == 'week':
        # Fetch weekly data (e.g., last 7 days)
        bp_data = BloodPressure.query.filter(BloodPressure.user_id == current_user.id, BloodPressure.timestamp >= datetime.utcnow() - timedelta(days=7)).all()
    elif view == 'month':
        # Fetch monthly data (e.g., last 30 days)
        bp_data = BloodPressure.query.filter(BloodPressure.user_id == current_user.id, BloodPressure.timestamp >= datetime.utcnow() - timedelta(days=30)).all()
    else:
        bp_data = []

    bp_data_formatted = [{'timestamp': bp.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'systolic': bp.systolic, 'diastolic': bp.diastolic} for bp in bp_data]
    return jsonify(bp_data_formatted)


@main.route('/heart_rate', methods=['GET', 'POST'])
@login_required
def heart_rate():
    form = HeartRateForm()
    if form.validate_on_submit():
        hr = HeartRate(
            user_id=current_user.id,
            heart_rate=form.heart_rate.data,
        )
        db.session.add(hr)
        db.session.commit()
        return jsonify(success=True)
    elif request.method == 'POST':
        return jsonify(success=False, errors=form.errors)

    hr_data = HeartRate.query.filter_by(user_id=current_user.id).all()
    hr_data_formatted = [{'timestamp': hr.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'heart_rate': hr.heart_rate} for hr in hr_data]
    return render_template('heart_rate.html', form=form, hr_data=hr_data_formatted)

@main.route('/heart_rate_data', methods=['GET'])
@login_required
def heart_rate_data():
    view = request.args.get('view', 'day')
    
    if view == 'day':
        hr_data = HeartRate.query.filter_by(user_id=current_user.id).all()
    elif view == 'week':
        hr_data = HeartRate.query.filter(HeartRate.user_id == current_user.id, HeartRate.timestamp >= datetime.utcnow() - timedelta(days=7)).all()
    elif view == 'month':
        hr_data = HeartRate.query.filter(HeartRate.user_id == current_user.id, HeartRate.timestamp >= datetime.utcnow() - timedelta(days=30)).all()
    else:
        hr_data = []

    hr_data_formatted = [{'timestamp': hr.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'heart_rate': hr.heart_rate} for hr in hr_data]
    return jsonify(hr_data_formatted)


@main.route('/cholesterol', methods=['GET', 'POST'])
@login_required
def cholesterol():
    form = CholesterolForm()
    if form.validate_on_submit():
        cholesterol = Cholesterol(
            user_id=current_user.id,
            cholesterol_level=form.cholesterol_level.data,
        )
        db.session.add(cholesterol)
        db.session.commit()
        return jsonify(success=True)
    elif request.method == 'POST':
        return jsonify(success=False, errors=form.errors)

    cholesterol_data = Cholesterol.query.filter_by(user_id=current_user.id).all()
    cholesterol_data_formatted = [{'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'cholesterol_level': c.cholesterol_level} for c in cholesterol_data]
    return render_template('cholesterol.html', form=form, cholesterol_data=cholesterol_data_formatted)

@main.route('/cholesterol_data')
@login_required
def cholesterol_data():
    view = request.args.get('view', 'day')
    
    if view == 'day':
        cholesterol_data = Cholesterol.query.filter_by(user_id=current_user.id).all()
    elif view == 'week':
        cholesterol_data = Cholesterol.query.filter(Cholesterol.user_id == current_user.id, Cholesterol.timestamp >= datetime.utcnow() - timedelta(days=7)).all()
    elif view == 'month':
        cholesterol_data = Cholesterol.query.filter(Cholesterol.user_id == current_user.id, Cholesterol.timestamp >= datetime.utcnow() - timedelta(days=30)).all()
    else:
        cholesterol_data = []

    cholesterol_data_formatted = [{'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'cholesterol_level': c.cholesterol_level} for c in cholesterol_data]
    return jsonify(cholesterol_data_formatted)

@main.route('/glucose', methods=['GET', 'POST'])
@login_required
def glucose():
    form = GlucoseForm()
    if form.validate_on_submit():
        glucose = Glucose(
            user_id=current_user.id,
            glucose_level=form.glucose_level.data,
        )
        db.session.add(glucose)
        db.session.commit()
        return jsonify(success=True)
    elif request.method == 'POST':
        return jsonify(success=False, errors=form.errors)

    glucose_data = Glucose.query.filter_by(user_id=current_user.id).all()
    glucose_data_formatted = [{'timestamp': g.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'glucose_level': g.glucose_level} for g in glucose_data]
    return render_template('glucose.html', form=form, glucose_data=glucose_data_formatted)

@main.route('/glucose_data')
@login_required
def glucose_data():
    view = request.args.get('view', 'day')
    
    if view == 'day':
        glucose_data = Glucose.query.filter_by(user_id=current_user.id).all()
    elif view == 'week':
        glucose_data = Glucose.query.filter(Glucose.user_id == current_user.id, Glucose.timestamp >= datetime.utcnow() - timedelta(days=7)).all()
    elif view == 'month':
        glucose_data = Glucose.query.filter(Glucose.user_id == current_user.id, Glucose.timestamp >= datetime.utcnow() - timedelta(days=30)).all()
    else:
        glucose_data = []

    glucose_data_formatted = [{'timestamp': g.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'glucose_level': g.glucose_level} for g in glucose_data]
    return jsonify(glucose_data_formatted)

@main.route('/load_dashboard')
@login_required
def load_dashboard():
    return render_template('dashboard.html')
