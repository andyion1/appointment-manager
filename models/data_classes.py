# Might make user related stuff after.

class Appointment:
    def __init__(self, *args):
        self.user_id = args[0] 
        self.username = args[1]
        self.password_hash = args[2]
        self.email = args[3]
        self.full_name = args[4]
        self.role = args[5]

class Report:
    def __init__(self, *args):
        self.report_id = args[0]
        self.appointment_id = args[1]
        self.generated_by = args[2] 
        self.content = args[3]
        self.created_at = args[4]
        self.feedback = args[5] 
        self.teacher_response = args[6]