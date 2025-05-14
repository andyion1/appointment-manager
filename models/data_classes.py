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
        self.created_role = args[8]

        # Optional attributes (to be set later)
        self.student_name = None
        self.teacher_name = None
  


class Report:
    def __init__(self, report_id, generated_by, created_at, appointment_id, feedback=None, teacher_response=None):
        self.report_id = report_id
        self.generated_by = generated_by 
        self.created_at = created_at
        self.appointment_id = appointment_id
        self.feedback = feedback
        self.teacher_response = teacher_response

        # Optional attributes (to be set later)
        self.student_name = None
        self.teacher_name = None
