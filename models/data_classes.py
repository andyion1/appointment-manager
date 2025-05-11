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


class Report:
    def __init__(self, *args):
        self.report_id = args[0]
        self.appointment_id = args[1]
        self.generated_by = args[2] 
        self.content = args[3]
        self.created_at = args[4]
        self.feedback = args[5] 
        self.teacher_response = args[6]