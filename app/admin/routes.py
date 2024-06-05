from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import User
from app import db

admin = Blueprint('admin', __name__)

@admin.route('/admin/manage_staff')
@login_required
def manage_staff():
    staff = User.query.filter_by(role_A='Staff').all()
    return render_template('manage_staff.html', staff=staff)

@admin.route('/admin/manage_patients')
@login_required
def manage_patients():
    patients = User.query.filter_by(role_A='Patient').all()
    return render_template('manage_patients.html', patients=patients)

@admin.route('/admin/edit_role/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_role(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.role_B = request.form['role_B']
        user.role_C = request.form['role_C']
        db.session.commit()
        flash('Roles updated successfully!', 'success')
        return redirect(url_for('admin.manage_staff' if user.role_A == 'Staff' else 'admin.manage_patients'))

    return render_template('edit_role.html', user=user)
