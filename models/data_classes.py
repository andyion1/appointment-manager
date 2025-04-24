class User:
    def __init__(self, *args):
        self.user_id = args[0]
        self.username = args[1]
        self.password_hash = args[2]
        self.email = args[3]
        self.full_name = args[4]
        self.role = args[5]

class Student:
    def __init__(self, *args):
        self.student_id = args[0]
        self.user_id = args[1]
        self.program = args[2]
        self.student_number = args[3] if len(args) > 3 else None

class Teacher:
    def __init__(self, *args):
        self.teacher_id = args[0]
        self.user_id = args[1]
        self.department = args[2]
        self.office_location = args[3] if len(args) > 3 else None

class Appointment:
    def __init__(self, *args):
        self.student_id = args[0]
        self.teacher_id = args[1]
        self.appointment_date = args[2]
        self.appointment_time = args[3]
        self.reason = args[4]
        self.status = args[5]

class Report:
    def __init__(self, *args):
        self.report_id = args[0]
        self.appointment_id = args[1]
        self.generated_by = args[2] 
        self.content = args[3]
        self.created_at = args[4]
        self.feedback = args[5] 
        self.teacher_response = args[6]