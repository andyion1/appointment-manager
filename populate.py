from models.database import Database
from app.user.user import User  # Adjust the import path if needed

def populate_teachers():
    db = Database()

    teachers = [
        ("jdoe", "jdoe@example.com", "John Doe"),
        ("asmith", "asmith@example.com", "Alice Smith"),
        ("bnguyen", "bnguyen@example.com", "Bao Nguyen"),
        ("klam", "klam@example.com", "Kevin Lam"),
        ("tchan", "tchan@example.com", "Tina Chan")
    ]

    for username, email, full_name in teachers:
        User.create_user(username, "Password123!", email, full_name, "teacher")

    db.close()

if __name__ == "__main__":
    populate_teachers()
