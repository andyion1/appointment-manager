# Might make user related stuff after.

class Appointment:
    def __init__(self, *args):
        self.appointment_id = args[0]
        self.student_id = args[1]
        self.teacher_id = args[2]
        self.appointment_date = args[3]
        self.appointment_time = args[4]
        self.status = args[5]
        self.reason = args[6]
        self.created_at = args[7]

        # Optional attributes (to be set later)
        self.student_name = None
        self.teacher_name = None
  


class Report:
    def __init__(self, report_id, appointment_id, author_id, content, created_at, feedback=None, teacher_response=None):
        self.report_id = report_id
        self.appointment_id = appointment_id
        self.author_id = author_id
        self.content = content
        self.created_at = created_at
        self.feedback = feedback
        self.teacher_response = teacher_response

