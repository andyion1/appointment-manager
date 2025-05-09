import pdb
from app.user.user import User

def create_admin(username, password, email, full_name, role):
    admin = User.create_user(
        username=username,
        password=password,
        email=email,
        full_name=full_name,
        role=role
    )
    pdb.set_trace()
    if admin:
        print(f"{role} '{username}' created successfully.")
    else:
        print(f"{role} '{username}' already exists or failed to create.")

if __name__ == "__main__":
    create_admin("admin_user", "Password123!", "admin_user@example.com", "Admin User", "admin_user")
    create_admin("admin_appoint", "Password123!", "admin_appoint@example.com", "Appointment Admin", "admin_appoint")
    create_admin("superuser", "Password123!", "superuser@example.com", "Superuser", "superuser")
