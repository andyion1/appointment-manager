from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=50, message='Username must be between 3 and 50 characters')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=3, message='Password must be at least 3 characters')
    ])
    
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=50, message='Username must be between 3 and 50 characters')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Length(max=100, message='Email cannot exceed 100 characters')
    ])
    
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(max=100, message='Full name cannot exceed 100 characters')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=3, message='Password must be at least 3 characters')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    role = SelectField('User Type', choices=[
        ('student', 'Student'), 
        ('teacher', 'Teacher')
    ], validators=[DataRequired(message='Please select your role')])
    
    program = StringField('Program', validators=[
        Length(max=100, message='Program name cannot exceed 100 characters')
    ])
    
    student_number = StringField('Student Number', validators=[
        Length(max=20, message='Student number cannot exceed 20 characters')
    ])
    
    department = StringField('Department', validators=[
        Length(max=100, message='Department name cannot exceed 100 characters')
    ])
    
    office_location = StringField('Office Location', validators=[
        Length(max=50, message='Office location cannot exceed 50 characters')
    ])
    
    submit = SubmitField('Register')
class ProfileForm(FlaskForm):
    full_name = StringField('fname', validators=[
        DataRequired(),
        Length(min=3, max=25)
    ])
    email = EmailField('email', validators=[
        DataRequired(),
        Length(min=3, max=25)
    ])
    submit = SubmitField('Update')
