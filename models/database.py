import os
import sys

from models.data_classes import Appointment
from models.data_classes import Report
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from config import Config 
import pdb

class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def __connect(self):
        # write the command that return a connection to your database in cspostgres 
        # database server (use Config class defined in config.py).
        # remove the pass comand below
        conn = psycopg2.connect(
            dbname=Config.name,
            user=Config.user,
            password=Config.password,
            host=Config.host,
            port=Config.port
        )
        return conn
    
    def __reconnect(self):
        try:
            self.close()
        except psycopg2.Error as f:
            pass
        self.__connection = self.__connect()

    def  db_conn (self): 
        return self.__connection
    
    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def get_cursor(self):
            for i in range(3):
                try:
                    return self.__connection.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()

    def __run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    if line[:2]=='--': continue
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join( statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []
    
    def run_sql_script(self, sql_filename):
        if os.path.exists(sql_filename):
            self.__connect()
            self.__run_file(sql_filename)
            self.close()
        else:
            print('Invalid Path')

 # ===========================================================================
# ----------------DML  (CRUD) queries (retrieve, insert, update, delete -----
# ---------------------------------------------------------------------------


    def add_user(self, user):
        '''Add a user to the DB for the given User object (tuple)'''
        qry = f"INSERT INTO USER_PROJ (username, password_hash, email, full_name, role, user_image) VALUES ('{user.username}', '{user.password_hash}', '{user.email}', '{user.full_name}', '{user.role}', '{user.user_image}')"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                self.__connect()
            except Exception as e:
                print(e)

    def get_users(self):
        qry = "SELECT * FROM USER_PROJ"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                return curr.fetchall()
            except Exception as e:
                print("get_all_users error:", e)
                return []

    def get_user(self, cond):
        '''Returns a User object based on the provided user_id'''
        from app.user.user import User
        qry = f"SELECT user_id, username, password_hash, email, full_name, role, user_image, status, warned FROM USER_PROJ WHERE {cond}"

        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                user_data = curr.fetchone()
                if user_data:
                    return User(*user_data)
                return None
            except Exception as e:
                print(e)
    
    def update_user(self, id, updates):
        set_clauses = []
        for key, value in updates.items():
            if isinstance(value, str):
                set_clauses.append(f"{key} = '{value}'")
            elif isinstance(value, bool):
                set_clauses.append(f"{key} = {'TRUE' if value else 'FALSE'}")
            else:
                set_clauses.append(f"{key} = {value}")
        
        set_clause = ", ".join(set_clauses)
        qry = f"UPDATE USER_PROJ SET {set_clause} WHERE user_id = {id}"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
            except Exception as e:
                print("update_user error:", e)

    def delete_user(self, user_id):
        qry = "DELETE FROM USER_PROJ WHERE user_id = %s"
        with self.get_cursor() as curr:
            curr.execute(qry, (user_id,))


    def add_teacher(self, teacher):
        '''Add a teacher to the DB from a Teacher object'''
        qry = """
            INSERT INTO TEACHER (user_id, department, office_location)
            VALUES (%s, %s, %s)
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry, (teacher.user_id, teacher.department, teacher.office_location))
            except Exception as e:
                print("add_teacher error:", e)

    def get_teachers(self):
        """Returns all teachers as Teacher objects"""
        from app.user.user import Teacher
        query = """
            SELECT u.user_id, u.username, u.password_hash, u.email, u.full_name, u.role, u.user_image,
                t.teacher_id, t.department, t.office_location
            FROM USER_PROJ u
            JOIN TEACHER t ON u.user_id = t.user_id
            WHERE u.role = 'teacher'
            """
        with self.get_cursor() as curr:
            try:
                curr.execute(query)
                data = curr.fetchall()
                return [Teacher(*row) for row in data] if data else []
            except Exception as e:
                print("get_teachers error:", e)
                return []

    def get_teacher(self, cond):
        '''Returns a Teacher object based on a condition (e.g., teacher_id = 3)'''
        from app.user.user import Teacher
        qry = f"""
            SELECT u.user_id, u.username, u.password_hash, u.email, u.full_name, u.role, u.user_image,
                t.teacher_id, t.department, t.office_location
            FROM USER_PROJ u
            JOIN TEACHER t ON u.user_id = t.user_id
            WHERE {cond}
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                data = curr.fetchone()
                if data:
                    return Teacher(*data)
                return None
            except Exception as e:
                print("get_teacher error:", e)
                return None
        
    def add_student(self, student):
        '''Add a student to the DB from a Student object'''
        qry = """
            INSERT INTO STUDENT (user_id, program, student_number)
            VALUES (%s, %s, %s)
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry, (student.user_id, student.program, student.student_number))
            except Exception as e:
                print("add_student error:", e)


    def get_student(self, cond):
        '''Returns a Student object based on a condition (e.g., student_id = 3)'''
        from app.user.user import Student
        qry = f"""
            SELECT u.user_id, u.username, u.password_hash, u.email, u.full_name, u.role, u.user_image,
                s.student_id, s.program, s.student_number
            FROM USER_PROJ u
            JOIN Student s ON u.user_id = s.user_id
            WHERE {cond}
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                data = curr.fetchone()
                if data:
                    return Student(*data)
                return None
            except Exception as e:
                print("get_student error:", e)
                return None
    def get_students(self):
        from app.user.user import Student
        query = """
            SELECT u.user_id, u.username, u.password_hash, u.email, u.full_name, u.role, u.user_image,
                s.student_id, s.program, s.student_number
            FROM USER_PROJ u
            JOIN STUDENT s ON u.user_id = s.user_id
            WHERE u.role = 'student'
            """
        with self.get_cursor() as curr:
            try:
                curr.execute(query)
                data = curr.fetchall()
                return [Student(*row) for row in data] if data else []
            except Exception as e:
                print("get_students error:", e)
                return []

    def get_appointment(self, cond):
        '''Returns an Appointment object with student and teacher names'''
        qry = f"""
            SELECT a.appointment_id, a.student_id, a.teacher_id, 
                a.appointment_date, a.status, a.created_at, 
                a.appointment_time, a.reason,
                su.full_name AS student_name, 
                tu.full_name AS teacher_name
            FROM appointment a
            JOIN student s ON a.student_id = s.student_id
            JOIN teacher t ON a.teacher_id = t.teacher_id
            JOIN user_proj su ON s.user_id = su.user_id
            JOIN user_proj tu ON t.user_id = tu.user_id
            WHERE {cond}
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                data = curr.fetchone()
                if data:
                    return Appointment(*data)
                return None
            except Exception as e:
                print(f"get_appointment error: {e}")
                return None

    
    def add_appointment(self, appointment):
        '''Add an appointment to the database'''
        qry = """
            INSERT INTO APPOINTMENT (student_id, teacher_id, appointment_date, status, created_at, appointment_time, reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING appointment_id
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry, (
                    appointment.student_id, 
                    appointment.teacher_id, 
                    appointment.appointment_date, 
                    appointment.status, 
                    appointment.created_at, 
                    appointment.appointment_time, 
                    appointment.reason
                ))
                appointment_id = curr.fetchone()[0]
                return appointment_id
            except Exception as e:
                print("add_appointment error:", e)
                return None

    def get_appointments(self, cond=None):
        '''Returns all appointments as Appointment objects, with optional condition'''
        from models.data_classes import Appointment
        qry = "SELECT * FROM APPOINTMENT"
        if cond:
            qry += f" WHERE {cond}"
        qry += " ORDER BY appointment_date DESC, appointment_time ASC"
        
        with self.get_cursor() as curr:
            try:    
                curr.execute(qry)
                data = curr.fetchall()
                appointments = []
                for appointment in data:
                    appointments.append(Appointment(appointment[0], appointment[1], appointment[2], appointment[3], appointment[6], appointment[4], appointment[7], appointment[5]))
                return appointments if data else []
            except Exception as e:
                print("get_appointments error:", e)
                return []


    def get_appointments_with_details(self, cond=None):
        '''Returns appointments with student and teacher names'''
        qry = """
            SELECT a.appointment_id, a.student_id, a.teacher_id, a.appointment_date, 
                a.status, a.created_at, a.appointment_time, a.reason,
                su.full_name as student_name, tu.full_name as teacher_name
            FROM APPOINTMENT a
            JOIN STUDENT s ON a.student_id = s.student_id
            JOIN TEACHER t ON a.teacher_id = t.teacher_id
            JOIN USER_PROJ su ON s.user_id = su.user_id
            JOIN USER_PROJ tu ON t.user_id = tu.user_id
        """
        if cond:
            qry += f" WHERE {cond}"
        qry += " ORDER BY a.appointment_date DESC, a.appointment_time ASC"
        
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                appointments = [Appointment(*row) for row in curr.fetchall()]
                return appointments
            except Exception as e:
                print("get_appointments_with_details error:", e)
                return []
            
    def get_appointment_with_details(self, cond):
        '''Returns a single Appointment object with student and teacher full names'''
        qry = f"""
            SELECT a.appointment_id, a.student_id, a.teacher_id, 
                a.appointment_date, a.appointment_time, a.status, 
                a.reason, a.created_at,
                su.full_name as student_name, 
                tu.full_name as teacher_name
            FROM APPOINTMENT a
            JOIN STUDENT s ON a.student_id = s.student_id
            JOIN TEACHER t ON a.teacher_id = t.teacher_id
            JOIN USER_PROJ su ON s.user_id = su.user_id
            JOIN USER_PROJ tu ON t.user_id = tu.user_id
            WHERE {cond}
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                row = curr.fetchone()
                if row:
                    # first 8 values go into constructor
                    appointment = Appointment(*row[:8])
                    # set optional name fields
                    appointment.student_name = row[8]
                    appointment.teacher_name = row[9]
                    return appointment
                return None
            except Exception as e:
                print(f"get_appointment_with_details error: {e}")
                return None

    def update_appointment(self, appointment_id, updates):
        '''Update an appointment in the database'''
        set_clauses = []
        for key, value in updates.items():
            if isinstance(value, str):
                set_clauses.append(f"{key} = '{value}'")
            else:
                set_clauses.append(f"{key} = {value}")
        
        set_clause = ", ".join(set_clauses)
        qry = f"UPDATE APPOINTMENT SET {set_clause} WHERE appointment_id = {appointment_id}"
        
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                return True
            except Exception as e:
                print("update_appointment error:", e)
                return False

    def delete_appointment(self, appointment_id):
        '''Delete an appointment from the database'''
        qry = f"DELETE FROM APPOINTMENT WHERE appointment_id = {appointment_id}"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                return True
            except Exception as e:
                print("delete_appointment error:", e)
                return False
            
    def get_reports(self, cond=None):
        qry = "SELECT * FROM report"
        if cond:
            qry += f" WHERE {cond}"
        qry += " ORDER BY created_at DESC"
        with self.get_cursor() as curr:
            curr.execute(qry)
            return curr.fetchall()
        
    def get_reports_with_details(self, condition=None):
        '''Get reports with student and teacher full names'''
        qry = """
            SELECT 
                r.report_id,
                r.generated_by,
                r.content,
                r.created_at,
                r.appointment_id,
                r.feedback,
                r.teacher_response,
                su.full_name AS student_name,
                tu.full_name AS teacher_name
            FROM REPORT r
            JOIN APPOINTMENT a ON r.appointment_id = a.appointment_id
            JOIN STUDENT s ON a.student_id = s.student_id
            JOIN TEACHER t ON a.teacher_id = t.teacher_id
            JOIN USER_PROJ su ON s.user_id = su.user_id
            JOIN USER_PROJ tu ON t.user_id = tu.user_id
        """
        if condition:
            qry += f" WHERE {condition}"
        qry += " ORDER BY r.created_at DESC"

        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                rows = curr.fetchall()

                reports = []
                for row in rows:
                    report = Report(
                        report_id=row[0],
                        generated_by=row[1],
                        content=row[2],
                        created_at=row[3],
                        appointment_id=row[4],
                        feedback=row[5],
                        teacher_response=row[6]
                    )
                    report.student_name = row[7]
                    report.teacher_name = row[8]
                    reports.append(report)

                return reports
            except Exception as e:
                print("get_reports_with_details error:", e)
                return []



            
    def get_report(self, cond):
        '''Returns a Report object based on the provided condition'''
        from models.data_classes import Report
        qry = f"SELECT * FROM report WHERE {cond}"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                data = curr.fetchone()
                if data:
                    # Make sure the parameters match the order of columns in the database
                    return Report(
                        report_id=data[0],
                        generated_by=data[1],
                        content=data[2],
                        created_at=data[3],
                        appointment_id=data[4],
                        feedback=data[5],
                        teacher_response=data[6]
                    )
                return None
            except Exception as e:
                print(f"get_report error: {e}")
                return None
            
    def get_report_with_details(self, cond):
        '''Returns a single Report object with student and teacher full names'''
        qry = f"""
            SELECT 
                r.report_id,
                r.generated_by,
                r.content,
                r.created_at,
                r.appointment_id,
                r.feedback,
                r.teacher_response,
                su.full_name AS student_name,
                tu.full_name AS teacher_name
            FROM REPORT r
            JOIN APPOINTMENT a ON r.appointment_id = a.appointment_id
            JOIN STUDENT s ON a.student_id = s.student_id
            JOIN TEACHER t ON a.teacher_id = t.teacher_id
            JOIN USER_PROJ su ON s.user_id = su.user_id
            JOIN USER_PROJ tu ON t.user_id = tu.user_id
            WHERE {cond}
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                row = curr.fetchone()
                if row:
                    report = Report(
                        report_id=row[0],
                        generated_by=row[1],
                        content=row[2],
                        created_at=row[3],
                        appointment_id=row[4],
                        feedback=row[5],
                        teacher_response=row[6]
                    )
                    report.student_name = row[7]
                    report.teacher_name = row[8]
                    return report
                return None
            except Exception as e:
                print(f"get_report_with_details error: {e}")
                return None



    def add_report(self, report):
        '''Add a report to the database'''
        qry = """
            INSERT INTO report (appointment_id, generated_by, content, created_at, feedback, teacher_response)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING report_id
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry, (
                    report.appointment_id,    # Integer expected here
                    report.generated_by,      # Changed from author_id
                    report.content,
                    report.created_at,        # Added created_at parameter
                    report.feedback,
                    report.teacher_response
                ))
                report_id = curr.fetchone()[0]
                return report_id
            except Exception as e:
                print("add_report error:", e)
                return None
            
    def update_report(self, report_id, updates):
        '''Update a report in the database'''
        qry = """
            UPDATE REPORT
            SET content = %s,
                feedback = %s,
                teacher_response = %s
            WHERE report_id = %s
        """
        with self.get_cursor() as curr:
            try:
                curr.execute(qry, (
                    updates.get('content'),
                    updates.get('feedback'),
                    updates.get('teacher_response'),
                    report_id
                ))
                return curr.rowcount > 0
            except Exception as e:
                print("update_report error:", e)
                return False


# ===========================================================================
db = Database()

if __name__ == '__main__':
    db.run_sql_script('./models/database.sql')