from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class ReportForm(FlaskForm):
    appointment_id = HiddenField('Appointment ID')
    feedback = TextAreaField('Student Feedback')
    teacher_response = TextAreaField('Teacher Response')
    submit = SubmitField('Submit Report')