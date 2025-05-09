from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, PasswordField, DateField, TimeField
from wtforms.validators import DataRequired, Length, AnyOf, NumberRange, Optional, EqualTo

class AppointmentForm(FlaskForm):
    teacher = SelectField('Select Teacher', coerce=int, choices=[], validators=[DataRequired()])
    student = SelectField('Select Student', coerce=int, choices=[], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    reason = StringField('Reason / Notes', render_kw={"rows": 3})
    submit = SubmitField('Book Appointment')

class AppointmentStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')