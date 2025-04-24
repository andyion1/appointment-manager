class Appointment:
    def __init__(self, *args):
        self.student_id = args[0]
        self.teacher_id = args[1]
        self.appointment_date = args[2]
        self.appointment_time = args[3]
        self.reason = args[4]
        self.status = args[5]


