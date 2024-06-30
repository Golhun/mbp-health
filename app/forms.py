from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms import StringField, PasswordField, DateField, IntegerField, BooleanField, TextAreaField, FileField, SubmitField, SelectField, HiddenField, DecimalField

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):  # Renamed to avoid duplicate class names
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = HiddenField('Email', validators=[Optional(), Email()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    height = IntegerField('Height (cm)', validators=[Optional()])
    weight = IntegerField('Weight (kg)', validators=[Optional()])
    medications = TextAreaField('Medications', validators=[Length(max=500), Optional()])
    allergies = TextAreaField('Allergies', validators=[Length(max=500), Optional()])
    profile_picture = FileField('Profile Picture')
    old_password = PasswordField('Old Password')
    new_password = PasswordField('New Password', validators=[Optional(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[Optional()])
    submit = SubmitField('Update Profile')

class BloodPressureForm(FlaskForm):
    systolic = IntegerField('Systolic', validators=[DataRequired()])
    diastolic = IntegerField('Diastolic', validators=[DataRequired()])
    submit = SubmitField('Add Data')

class HeartRateForm(FlaskForm):
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    submit = SubmitField('Add Heart Rate')

class CholesterolForm(FlaskForm):
    cholesterol_level = IntegerField('Cholesterol Level', validators=[DataRequired()])
    submit = SubmitField('Add Cholesterol')

class GlucoseForm(FlaskForm):
    glucose_level = DecimalField('Glucose Level', validators=[DataRequired()])
    submit = SubmitField('Add Data')

class LogoutForm(FlaskForm):
    pass