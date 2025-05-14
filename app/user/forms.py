from flask_wtf import FlaskForm
from wtforms import EmailField, FileField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from flask_wtf.file import FileRequired, FileAllowed

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

class StudentExtraForm(FlaskForm):
    program = StringField("Program", validators=[DataRequired()])
    student_number = StringField("Student Number", validators=[DataRequired()])
    submit = SubmitField("Complete Registration")

class TeacherExtraForm(FlaskForm):
    department = StringField("Department")
    office_location = StringField("Office Location")
    submit = SubmitField("Complete Registration")

class ProfileForm(FlaskForm):
    full_name = StringField('Enter New Full Name', validators=[
        Optional(),
        Length(min=3, max=25)
    ])
    email = EmailField('Enter New Email', validators=[
        Optional(),
        Length(min=3, max=25)
    ])
    user_image = FileField('Upload New Image Profile Picture', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Only image files are allowed!'), Optional()
    ])

    submit = SubmitField('Update')
