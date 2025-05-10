# Might make user related stuff after.

class Appointment:
    def __init__(self, appointment_id, student_name, teacher_name, appointment_date, status, created_at, appointment_time, reason):
        self.appointment_id = appointment_id
        self.student_name = student_name
        self.teacher_name = teacher_name
        self.appointment_date = appointment_date
        self.status = status
        self.created_at = created_at
        self.appointment_time = appointment_time
        self.reason = reason


class Report:
    def __init__(self, *args):
        self.report_id = args[0]
        self.appointment_id = args[1]
        self.generated_by = args[2] 
        self.content = args[3]
        self.created_at = args[4]
        self.feedback = args[5] 
        self.teacher_response = args[6]