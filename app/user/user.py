from flask import flash, request
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from datetime import datetime
import pdb

class User(UserMixin):
    def __init__(self, *args):
        self.user_id = args[0] 
        self.username = args[1] 
        self.password_hash = args[2]
        self.email = args[3]
        self.full_name = args[4]
        self.role = args[5]
        self.user_image = args[6] if len(args) > 6 else None
        self.status = args[7] if len(args) > 7 else 'active'
        self.warned = args[8] if len(args) > 8 else False
    
    
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def create_user(username, password, email, full_name, role):
        """Creates a new user in the database"""
        # Check if username already exists
        existing_user = User.get_user_by_username(username)
        if existing_user:
            flash("This username is already taken.", "danger")
            return None
        
        # Check if email already exists
        existing_email = User.get_user_by_email(email)
        if existing_email:
            flash("This email is already registered.", "danger")
            return None
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        user = User(0, username, hashed_password, email, full_name, role)
        
        # Add user to database
        db.add_user(user)
        user = User.get_user_by_username(username)
        return user
       
    
    @staticmethod
    def get_user_by_id(user_id):
        """Fetches a user by their ID"""
        cond = f"user_id = {user_id}"
        return db.get_user(cond)
    
    @staticmethod
    def update_user(id, email=None, full_name=None):
        """Updates user information"""
        updates = {}
        
        if email:
            updates['email'] = email
        
        if full_name:
            updates['full_name'] = full_name
        
        if updates:
            db.update_user(id, updates)   
    
    @staticmethod
    def get_user_by_username(username):
        """Fetches a user by their username"""
        cond = f"username = '{username}'"
        return db.get_user(cond)
    
    @staticmethod
    def get_user_by_email(email):
        """Fetches a user by their email"""
        cond = f"email = '{email}'"
        return db.get_user(cond)
    
    def update_password(self, new_password):
        """Updates user password"""
        hashed_password = generate_password_hash(new_password)
        db.update_user_password(self.user_id, hashed_password)
    
    def check_password(self, password):
        """Checks if provided password matches stored hash"""
        return check_password_hash(self.password_hash, password)


class Student(User):
    def __init__(self, *args):
        super().__init__(*args[:7])  # Pass first 6 arguments to parent class
        
        # Student-specific attributes
        if len(args) >= 9:
            self.student_id = args[7]
            self.program = args[8]
            self.student_number = args[9] if len(args) > 8 else None
    
    @staticmethod
    def create_student(username, password, email, full_name, program, student_number=None):
        # Create base user with 'student' role
        user = User.get_user_by_username(username)

        if user:
            # Create full student object using base user
            student = Student(
                user.user_id,
                user.username,
                user.password_hash,
                user.email,
                user.full_name,
                user.role,
                None,
                None,
                program,
                student_number
            )

            # Add to DB
            db.add_student(student)

            # Return complete student object (in case the DB autogenerates any fields)
            return Student.get_student_by_user_id(user.user_id)

        return None

    #@staticmethod
    #def get_student_by_user_id(user_id):
     #   """Fetches a student by their user ID"""
      #  return db.get_student(f"user_id = {user_id}")
    
    @staticmethod
    def get_student_by_user_name(username):
        """Fetches a student by their username"""
        user = User.get_user_by_username(username)
        if user:
            return db.get_student(f"username = '{username}'")
        return None


class Teacher(User):
    def __init__(self, user_id=None, username=None, password_hash=None, email=None, full_name=None, role=None, user_image=None, teacher_id=None, department=None, office_location=None):
        # Initialize base User attributes
        super().__init__(user_id, username, password_hash, email, full_name, role, user_image)
        
        # Teacher-specific attributes
        self.teacher_id = teacher_id
        self.department = department
        self.office_location = office_location
    
    @staticmethod
    def create_teacher(username, password, email, full_name, department, office_location=None):
        user = User.get_user_by_username(username)
        if user:
            teacher = Teacher(
                user.user_id,
                user.username,
                user.password_hash,
                user.email,
                user.full_name,
                user.role,
                None,
                None,
                department,
                office_location
            )
            db.add_teacher(teacher)
            return Teacher.get_teacher_by_user_id(user.user_id)

        return None

    
    @staticmethod
    def get_teacher_by_user_id(user_id):
        """Fetches a teacher by their user ID"""
        user = User.get_user_by_id(user_id)
        if user:
            return db.get_teacher(f"user_id = {user_id}")
        return None
    
    @staticmethod
    def get_teacher_by_user_name(username):
        """Fetches a studteacherent by their username"""
        user = User.get_user_by_username(username)
        if user:
            return db.get_teacher(f"username = '{username}'")
        return None



# Admin User Classes
class AdminUser(User):
    @staticmethod
    def get_admin_by_user_id(user_id):
        """Fetches an admin by their user ID"""
        user = User.get_user_by_id(user_id)
        if user and user.role == 'admin_user':
            return user
        return None
        
class AdminAppointment(User):
    @staticmethod
    def get_admin_by_user_id(user_id):
        """Fetches an appointment admin by their user ID"""
        user = User.get_user_by_id(user_id)
        if user and user.role == 'admin_appoint':
            return user
        return None
        
class SuperUser(User):
    @staticmethod
    def get_admin_by_user_id(user_id):
        """Fetches a superuser by their user ID"""
        user = User.get_user_by_id(user_id)
        if user and user.role == 'superuser':
            return user
        return None