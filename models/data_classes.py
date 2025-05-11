# Might make user related stuff after.

class Appointment:
    def __init__(self, appointment_id, student_id, teacher_id, appointment_date,
                 status, created_at, appointment_time, reason,
                 student_name, teacher_name):
        self.appointment_id = appointment_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.appointment_date = appointment_date
        self.status = status
        self.created_at = created_at
        self.appointment_time = appointment_time
        self.reason = reason
        self.student_name = student_name
        self.teacher_name = teacher_name    


class Report:
    def __init__(self, report_id, appointment_id, author_id, content, created_at, updated_at):
        self.report_id = report_id
        self.appointment_id = appointment_id
        self.author_id = author_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
