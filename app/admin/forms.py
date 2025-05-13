from flask_wtf import FlaskForm
from wtforms import EmailField, FileField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileRequired, FileAllowed


class AdminCreationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=50)
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Length(max=100)
    ])
    
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=3)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    role = SelectField('Admin Role', choices=[
        ('admin_user', 'Admin User'), 
        ('admin_appoint', 'Admin Appoint')
    ], validators=[DataRequired(message='Please select an admin role')])
    
    submit = SubmitField('Create Admin')
