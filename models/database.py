import os
import sys
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
        qry = f"SELECT * FROM USER_PROJ WHERE {cond}"
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
        qry = f"update user_proj set full_name = '{updates['full_name']}', email = '{updates['email']}', user_image = '{updates['user_image']}' where user_id = '{id}'"
        with self.__connection.cursor() as curr:
            try:
                res = curr.execute(qry)
                self.__connection.commit()
            except Exception as e:
                print(e)

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
                pdb.set_trace()
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
        '''Returns a Student object based on the provided condition'''
        from app.user.user import Student
        qry = f"SELECT * FROM Student WHERE {cond}"
        with self.get_cursor() as curr:
            try:
                curr.execute(qry)
                student_data = curr.fetchone()
                if student_data:
                    return Student(*student_data)
                return None
            except Exception as e:
                print(e)
                return None
# ===========================================================================
db = Database()

if __name__ == '__main__':
    db.run_sql_script('./models/database.sql')