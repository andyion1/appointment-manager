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
    def to_dict(self):
        # Import here if needed
        import datetime

        # appointment_date and created_at could be datetime/date or strings
        # appointment_time could be time or string

        def format_time(value):
            if isinstance(value, datetime.time):
                return value.strftime("%H:%M:%S")
            return value  # assume it's already a string

        def format_date(value):
            if hasattr(value, 'isoformat'):
                return value.isoformat()
            return value  # assume it's already a string

        return {
            "appointment_id": self.appointment_id,
            "student_id": self.student_id,
            "teacher_id": self.teacher_id,
            "appointment_date": format_date(self.appointment_date),
            "appointment_time": format_time(self.appointment_time),
            "status": self.status,
            "reason": self.reason,
            "created_at": format_date(self.created_at),
            "created_role": self.created_role,
            "student_name": self.student_name,
            "teacher_name": self.teacher_name
        }

    


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
    
    def to_dict(self):
        return {
            "report_id": self.report_id,
            "generated_by": self.generated_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "appointment_id": self.appointment_id,
            "feedback": self.feedback,
            "teacher_response": self.teacher_response,
            "student_name": self.student_name,
            "teacher_name": self.teacher_name
        }
