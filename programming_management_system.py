import os
import sys
from datetime import datetime

# SYMBOLIC CONSTANTS
ADMIN_ROLE = "a"
TRAINER_ROLE = "b"
LECTURER_ROLE = "c"
STUDENT_ROLE = "d"

# Get the directory where this Python script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create file paths relative to script directory
USER_FILE = os.path.join(SCRIPT_DIR, "apu_list.txt")
TRAINERS_FILE = os.path.join(SCRIPT_DIR, "trainerslist.txt")
TRAINER_MODULES_FILE = os.path.join(SCRIPT_DIR, "trainermodules.txt")
STUDENTS_FILE = os.path.join(SCRIPT_DIR, "zstudents.txt")
REQUESTS_FILE = os.path.join(SCRIPT_DIR, "zrequests.txt")
FEEDBACK_FILE = os.path.join(SCRIPT_DIR, "feedback.txt")

MAX_LOGIN_ATTEMPTS = 3
LEVELS = ["Beginner", "Intermediate", "Advanced"]

def create_files_if_not_exist():
    """Create necessary files if they don't exist and create default admin"""
    files = [USER_FILE, TRAINERS_FILE, TRAINER_MODULES_FILE, STUDENTS_FILE, REQUESTS_FILE, FEEDBACK_FILE]
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass
    
    # Create default admin account if no users exist
    if not os.path.exists(USER_FILE) or os.path.getsize(USER_FILE) == 0:
        with open(USER_FILE, 'w') as f:
            f.write("admin,admin@apu.edu.my,admin123,a\n")
        print("Default admin account created:")
        print("Email: admin@apu.edu.my")
        print("Password: admin123")

def validate_email(email):
    """Validate email format"""
    return "@" in email and "." in email

def validate_level(level):
    """Validate coaching level"""
    return level in LEVELS

def get_user_input(prompt, validation_func=None, error_msg="Invalid input. Please try again."):
    """Get validated user input"""
    while True:
        user_input = input(prompt).strip()
        if validation_func is None or validation_func(user_input):
            return user_input
        print(error_msg)

def generate_student_id():
    """Generate unique student ID"""
    try:
        with open(STUDENTS_FILE, 'r') as f:
            lines = f.readlines()
            if lines:
                return f"STU{len(lines) + 1:04d}"
            else:
                return "STU0001"
    except FileNotFoundError:
        return "STU0001"

def main_menu():
    """Main system menu - login only (no registration)"""
    create_files_if_not_exist()
    print("=== APU Programming Café Management System ===")
    
    while True:
        print("\n1. Login")
        print("2. Exit")
        
        option = get_user_input("Enter your choice (1-2): ", 
                               lambda x: x in ['1', '2'],
                               "Invalid choice. Please enter 1 or 2.")
        
        if option == '1':
            login()
        elif option == '2':
            print("Thank you for using APU Programming Café Management System!")
            sys.exit()

def login():
    """User login function with role-based access"""
    print("\n=== User Login ===")
    login_attempts = 0
    
    while login_attempts < MAX_LOGIN_ATTEMPTS:
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        try:
            with open(USER_FILE, 'r') as f:
                for line in f:
                    user_info = line.strip().split(',')
                    if len(user_info) >= 4 and user_info[1] == email and user_info[2] == password:
                        print(f"Login successful! Welcome {user_info[0]}")
                        
                        # Route to appropriate role menu
                        if user_info[3] == ADMIN_ROLE:
                            admin_menu(user_info[0])
                        elif user_info[3] == TRAINER_ROLE:
                            trainer_menu(user_info[0])
                        elif user_info[3] == LECTURER_ROLE:
                            lecturer_menu(user_info[0])
                        elif user_info[3] == STUDENT_ROLE:
                            student_menu(user_info[0])
                        return
                        
                login_attempts += 1
                remaining = MAX_LOGIN_ATTEMPTS - login_attempts
                if remaining > 0:
                    print(f"Invalid credentials. You have {remaining} attempts left.")
                else:
                    print("Login failed. Maximum number of attempts reached.")
                    return
                    
        except FileNotFoundError:
            print("Error: User database not found.")
            return

# ============= ADMINISTRATOR FUNCTIONS =============

def admin_menu(admin_name):
    """Administrator main menu - ONLY admin can manage users"""
    while True:
        print(f"\n=== Administrator Menu - {admin_name} ===")
        print("1. Register new user (Admin/Trainer/Lecturer/Student)")
        print("2. Delete user")
        print("3. Register trainer") 
        print("4. Delete trainer")
        print("5. Assign trainer to module")
        print("6. View monthly income report")
        print("7. View feedback by trainer")
        print("8. Update own profile")
        print("9. Logout")
        print("10. Exit")
        
        choice = get_user_input("Enter your choice (1-10): ",
                               lambda x: x in ['1','2','3','4','5','6','7','8','9','10'],
                               "Invalid choice. Please enter 1-10.")
        
        if choice == "1":
            admin_register_user()
        elif choice == "2":
            admin_delete_user()
        elif choice == "3":
            register_trainer()
        elif choice == "4":
            delete_trainer()
        elif choice == "5":
            assign_trainer()
        elif choice == "6":
            view_monthly_income()
        elif choice == "7":
            view_feedback()
        elif choice == "8":
            update_profile(admin_name)
        elif choice == "9":
            return
        elif choice == "10":
            sys.exit()

def admin_register_user():
    """Admin registers new users for all roles"""
    print("\n=== Register New User (Admin Only) ===")
    
    username = get_user_input("Enter username: ", 
                             lambda x: len(x) >= 3,
                             "Username must be at least 3 characters long.")
    
    email = get_user_input("Enter email: ",
                          validate_email,
                          "Please enter a valid email address.")
    
    password = get_user_input("Enter password: ",
                             lambda x: len(x) >= 6,
                             "Password must be at least 6 characters long.")
    
    print("\nSelect role:")
    print("a - Administrator")
    print("b - Trainer") 
    print("c - Lecturer")
    print("d - Student")
    
    role = get_user_input("Enter role (a/b/c/d): ",
                         lambda x: x in [ADMIN_ROLE, TRAINER_ROLE, LECTURER_ROLE, STUDENT_ROLE],
                         "Please enter a valid role (a/b/c/d).")

    # Check if user already exists
    try:
        with open(USER_FILE, 'r') as f:
            for line in f:
                user_info = line.strip().split(',')
                if len(user_info) >= 2 and (user_info[0] == username or user_info[1] == email):
                    print("Error: Username or email already exists.")
                    return
    except FileNotFoundError:
        pass

    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{email},{password},{role}\n")

    role_names = {ADMIN_ROLE: "Administrator", TRAINER_ROLE: "Trainer", 
                 LECTURER_ROLE: "Lecturer", STUDENT_ROLE: "Student"}
    print(f"{role_names[role]} '{username}' registered successfully.")

def admin_delete_user():
    """Admin deletes users"""
    print("\n=== Delete User (Admin Only) ===")
    
    # Display all users
    try:
        with open(USER_FILE, 'r') as f:
            users = f.readlines()
            
        if not users:
            print("No users found.")
            return
            
        print("Current users:")
        role_names = {ADMIN_ROLE: "Administrator", TRAINER_ROLE: "Trainer", 
                     LECTURER_ROLE: "Lecturer", STUDENT_ROLE: "Student"}
        
        for i, line in enumerate(users, 1):
            user_info = line.strip().split(',')
            if len(user_info) >= 4:
                role_name = role_names.get(user_info[3], "Unknown")
                print(f"{i}. {user_info[0]} ({user_info[1]}) - {role_name}")
        
        username_to_delete = input("\nEnter username to delete: ").strip()
        
        # Find and remove user
        original_count = len(users)
        filtered_users = []
        deleted_user = None
        
        for line in users:
            user_info = line.strip().split(',')
            if len(user_info) >= 4 and user_info[0] != username_to_delete:
                filtered_users.append(line)
            elif len(user_info) >= 4 and user_info[0] == username_to_delete:
                deleted_user = user_info
        
        if len(filtered_users) < original_count:
            with open(USER_FILE, 'w') as f:
                f.writelines(filtered_users)
            print(f"User '{username_to_delete}' deleted successfully.")
        else:
            print("User not found.")
            
    except FileNotFoundError:
        print("User database not found.")

def register_trainer():
    """Register a new trainer to trainer list"""
    print("\n=== Register Trainer ===")
    
    trainer_name = get_user_input("Enter trainer name: ",
                                 lambda x: len(x) >= 2,
                                 "Trainer name must be at least 2 characters.")
    
    # Check if trainer already exists
    try:
        with open(TRAINERS_FILE, 'r') as f:
            trainers = f.read().splitlines()
            if trainer_name in trainers:
                print("Error: Trainer already exists in trainer list.")
                return
    except FileNotFoundError:
        trainers = []
    
    trainers.append(trainer_name)
    
    with open(TRAINERS_FILE, 'w') as f:
        for trainer in trainers:
            if trainer.strip():
                f.write(f"{trainer}\n")
    
    print("Trainer added to trainer list successfully.")

def delete_trainer():
    """Delete a trainer from trainer list"""
    print("\n=== Delete Trainer ===")
    
    try:
        with open(TRAINERS_FILE, 'r') as f:
            trainers = f.read().splitlines()
            trainers = [t for t in trainers if t.strip()]
    except FileNotFoundError:
        print("No trainers found.")
        return
    
    if not trainers:
        print("No trainers available to delete.")
        return
    
    print("Available trainers:")
    for i, trainer in enumerate(trainers, 1):
        print(f"{i}. {trainer}")
    
    trainer_name = input("Enter trainer name to delete: ").strip()
    
    if trainer_name in trainers:
        trainers.remove(trainer_name)
        
        with open(TRAINERS_FILE, 'w') as f:
            for trainer in trainers:
                if trainer.strip():
                    f.write(f"{trainer}\n")
        
        print("Trainer deleted from trainer list successfully.")
    else:
        print("Trainer not found.")

def assign_trainer():
    """Assign trainer to a module and level"""
    print("\n=== Assign Trainer to Module ===")
    
    # Display available trainers
    try:
        with open(TRAINERS_FILE, 'r') as f:
            trainers = f.read().splitlines()
            trainers = [t for t in trainers if t.strip()]
    except FileNotFoundError:
        print("No trainers found. Please register trainers first.")
        return
    
    if not trainers:
        print("No trainers available.")
        return
    
    print("Available trainers:")
    for trainer in trainers:
        print(f"- {trainer}")
    
    module = get_user_input("Enter module name: ",
                           lambda x: len(x) >= 2,
                           "Module name must be at least 2 characters.")
    
    trainer = get_user_input("Enter trainer name: ",
                           lambda x: x in trainers,
                           f"Trainer must be one of: {', '.join(trainers)}")
    
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    charges = get_user_input("Enter charges (RM): ",
                           lambda x: x.replace('.', '').isdigit(),
                           "Please enter a valid amount.")

    with open(TRAINER_MODULES_FILE, 'a') as f:
        f.write(f"{module},{trainer},{level},{charges},TBD\n")
    
    print("Trainer assigned to module successfully.")

def view_monthly_income():
    """View monthly income report"""
    print("\n=== Monthly Income Report ===")
    
    trainer_name = input("Enter trainer name: ").strip()
    module_name = input("Enter module name: ").strip()
    level = input("Enter level: ").strip()
    
    try:
        # Count paid students
        student_count = 0
        with open(STUDENTS_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 10 and fields[2] == module_name and fields[3] == level and fields[4] == trainer_name and fields[9] == "paid":
                    student_count += 1
        
        # Get charges from trainer modules
        charges = 0
        found = False
        with open(TRAINER_MODULES_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 4 and fields[0] == module_name and fields[1] == trainer_name and fields[2] == level:
                    charges = float(fields[3])
                    found = True
                    break
        
        if found:
            total_income = charges * student_count
            print(f"\nTrainer: {trainer_name}")
            print(f"Module: {module_name}")
            print(f"Level: {level}")
            print(f"Charges per student: RM{charges:.2f}")
            print(f"Number of paid students: {student_count}")
            print(f"Total monthly income: RM{total_income:.2f}")
        else:
            print("No matching trainer/module/level found.")
            
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except ValueError:
        print("Error: Invalid charges format in database.")

def view_feedback():
    """View feedback from trainers"""
    print("\n=== Trainer Feedback ===")
    
    try:
        with open(FEEDBACK_FILE, 'r') as f:
            feedback = f.readlines()
            if feedback:
                for line in feedback:
                    print(line.strip())
            else:
                print("No feedback available.")
    except FileNotFoundError:
        print("No feedback file found.")

def update_profile(username):
    """Update user profile"""
    print(f"\n=== Update Profile - {username} ===")
    
    try:
        with open(USER_FILE, 'r') as f:
            users = f.readlines()
        
        updated = False
        for i, line in enumerate(users):
            user_data = line.strip().split(',')
            if len(user_data) >= 4 and user_data[0] == username:
                print("Current profile:")
                print(f"Username: {user_data[0]}")
                print(f"Email: {user_data[1]}")
                
                new_email = input("Enter new email (leave blank to keep current): ").strip()
                if new_email:
                    if validate_email(new_email):
                        user_data[1] = new_email
                    else:
                        print("Invalid email format. Email not updated.")
                
                new_password = input("Enter new password (leave blank to keep current): ").strip()
                if new_password:
                    if len(new_password) >= 6:
                        user_data[2] = new_password
                    else:
                        print("Password too short. Password not updated.")
                
                users[i] = ",".join(user_data) + "\n"
                updated = True
                break
        
        if updated:
            with open(USER_FILE, 'w') as f:
                f.writelines(users)
            print("Profile updated successfully.")
        else:
            print("User profile not found.")
            
    except FileNotFoundError:
        print("User database not found.")

# ============= TRAINER FUNCTIONS =============
# ONLY functions that trainers can perform according to assignment

def trainer_menu(trainer_name):
    """Trainer main menu - restricted to trainer-only functions"""
    while True:
        print(f"\n=== Trainer Menu - {trainer_name} ===")
        
        # Display assigned modules
        display_trainer_modules(trainer_name)
        
        print("\nTrainer Functions:")
        print("1. Add coaching class information")
        print("2. Update coaching class information") 
        print("3. Delete coaching class information")
        print("4. View enrolled students")
        print("5. Send feedback to administrator")
        print("6. Update profile")
        print("7. Logout")
        print("8. Exit")
        
        choice = get_user_input("Enter your choice (1-8): ",
                               lambda x: x in ['1','2','3','4','5','6','7','8'],
                               "Invalid choice. Please enter 1-8.")
        
        if choice == "1":
            add_coaching_info(trainer_name)
        elif choice == "2":
            update_coaching_info(trainer_name)
        elif choice == "3":
            delete_coaching_info(trainer_name)
        elif choice == "4":
            view_enrolled_students(trainer_name)
        elif choice == "5":
            send_feedback(trainer_name)
        elif choice == "6":
            update_profile(trainer_name)
        elif choice == "7":
            return
        elif choice == "8":
            sys.exit()

def display_trainer_modules(trainer_name):
    """Display modules assigned to trainer"""
    print(f"\nModules assigned to {trainer_name}:")
    
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            found = False
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 3 and fields[1] == trainer_name:
                    charges = fields[3] if len(fields) > 3 else 'TBD'
                    schedule = fields[4] if len(fields) > 4 else 'TBD'
                    print(f"- {fields[0]} ({fields[2]}) - Charges: RM{charges} - Schedule: {schedule}")
                    found = True
            
            if not found:
                print("No modules assigned to you yet.")
    except FileNotFoundError:
        print("No module assignments found.")

def add_coaching_info(trainer_name):
    """Add coaching class information"""
    print("\n=== Add Coaching Class Information ===")
    
    print("1. Add schedule")
    print("2. Add charges")
    choice = get_user_input("Enter your choice (1-2): ",
                           lambda x: x in ['1', '2'],
                           "Please enter 1 or 2.")
    
    if choice == '1':
        add_schedule(trainer_name)
    elif choice == '2':
        add_charges(trainer_name)

def add_schedule(trainer_name):
    """Add schedule to coaching class"""
    module = input("Enter module name: ").strip()
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            data = f.readlines()
        
        updated = False
        for i, line in enumerate(data):
            fields = line.strip().split(",")
            if len(fields) >= 3 and fields[1] == trainer_name and fields[0] == module and fields[2] == level:
                schedule = input("Enter the schedule: ").strip()
                
                # Ensure we have at least 5 fields
                while len(fields) < 5:
                    fields.append("TBD")
                
                fields[4] = schedule
                data[i] = ",".join(fields) + "\n"
                updated = True
                break
        
        if updated:
            with open(TRAINER_MODULES_FILE, "w") as f:
                f.writelines(data)
            print("Schedule added successfully.")
        else:
            print("Module assignment not found for you.")
            
    except FileNotFoundError:
        print("Trainer modules file not found.")

def add_charges(trainer_name):
    """Add charges to coaching class"""
    module = input("Enter module name: ").strip()
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    charges = get_user_input("Enter charges (RM): ",
                           lambda x: x.replace('.', '').isdigit(),
                           "Please enter a valid amount.")
    
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            data = f.readlines()
        
        updated = False
        for i, line in enumerate(data):
            fields = line.strip().split(",")
            if len(fields) >= 3 and fields[1] == trainer_name and fields[0] == module and fields[2] == level:
                # Ensure we have at least 4 fields
                while len(fields) < 4:
                    fields.append("TBD")
                
                fields[3] = charges
                data[i] = ",".join(fields) + "\n"
                updated = True
                break
        
        if updated:
            with open(TRAINER_MODULES_FILE, "w") as f:
                f.writelines(data)
            print("Charges added successfully.")
        else:
            print("Module assignment not found for you.")
            
    except FileNotFoundError:
        print("Trainer modules file not found.")

def update_coaching_info(trainer_name):
    """Update coaching class information"""
    print("\n=== Update Coaching Class Information ===")
    
    print("1. Update charges")
    print("2. Update schedule")
    choice = get_user_input("Enter your choice (1-2): ",
                           lambda x: x in ['1', '2'],
                           "Please enter 1 or 2.")
    
    if choice == '1':
        update_charges(trainer_name)
    elif choice == '2':
        update_schedule(trainer_name)

def update_charges(trainer_name):
    """Update charges for coaching class"""
    module = input("Enter module name: ").strip()
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    new_charges = get_user_input("Enter new charges (RM): ",
                               lambda x: x.replace('.', '').isdigit(),
                               "Please enter a valid amount.")
    
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            data = f.readlines()
        
        updated = False
        for i, line in enumerate(data):
            fields = line.strip().split(",")
            if len(fields) >= 3 and fields[1] == trainer_name and fields[0] == module and fields[2] == level:
                while len(fields) < 4:
                    fields.append("TBD")
                fields[3] = new_charges
                data[i] = ",".join(fields) + "\n"
                updated = True
                break
        
        if updated:
            with open(TRAINER_MODULES_FILE, "w") as f:
                f.writelines(data)
            print("Charges updated successfully.")
        else:
            print("Module assignment not found for you.")
            
    except FileNotFoundError:
        print("Trainer modules file not found.")

def update_schedule(trainer_name):
    """Update schedule for coaching class"""
    module = input("Enter module name: ").strip()
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    new_schedule = input("Enter new schedule: ").strip()
    
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            data = f.readlines()
        
        updated = False
        for i, line in enumerate(data):
            fields = line.strip().split(",")
            if len(fields) >= 3 and fields[1] == trainer_name and fields[0] == module and fields[2] == level:
                while len(fields) < 5:
                    fields.append("TBD")
                fields[4] = new_schedule
                data[i] = ",".join(fields) + "\n"
                updated = True
                break
        
        if updated:
            with open(TRAINER_MODULES_FILE, "w") as f:
                f.writelines(data)
            print("Schedule updated successfully.")
        else:
            print("Module assignment not found for you.")
            
    except FileNotFoundError:
        print("Trainer modules file not found.")

def delete_coaching_info(trainer_name):
    """Delete coaching class information"""
    print("\n=== Delete Coaching Class ===")
    
    module = input("Enter module name to delete: ").strip()
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    confirm = input(f"Are you sure you want to delete {module} ({level})? (y/n): ").strip().lower()
    
    if confirm == 'y':
        try:
            with open(TRAINER_MODULES_FILE, "r") as f:
                data = f.readlines()
            
            original_count = len(data)
            filtered_data = []
            
            for line in data:
                fields = line.strip().split(",")
                if not (len(fields) >= 3 and fields[1] == trainer_name and fields[0] == module and fields[2] == level):
                    filtered_data.append(line)
            
            if len(filtered_data) < original_count:
                with open(TRAINER_MODULES_FILE, "w") as f:
                    f.writelines(filtered_data)
                print("Coaching class deleted successfully.")
            else:
                print("Coaching class not found for you.")
                
        except FileNotFoundError:
            print("Trainer modules file not found.")
    else:
        print("Deletion cancelled.")

def view_enrolled_students(trainer_name):
    """View students enrolled and paid for trainer's modules"""
    print(f"\n=== Students Enrolled for {trainer_name} ===")
    
    try:
        with open(STUDENTS_FILE, "r") as f:
            found = False
            print("Paid Students:")
            print("-" * 80)
            print(f"{'Name':<15} {'TP Number':<10} {'Module':<15} {'Level':<12} {'Charges':<10} {'Status'}")
            print("-" * 80)
            
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 10 and fields[4] == trainer_name and fields[9] == "paid":
                    print(f"{fields[0]:<15} {fields[1]:<10} {fields[2]:<15} {fields[3]:<12} RM{fields[8]:<8} {fields[9]}")
                    found = True
            
            if not found:
                print("No paid students found for your modules.")
                
    except FileNotFoundError:
        print("Students file not found.")

def send_feedback(trainer_name):
    """Send feedback to administrator"""
    print("\n=== Send Feedback to Administrator ===")
    
    feedback = get_user_input("Enter your feedback: ",
                            lambda x: len(x) >= 5,
                            "Feedback must be at least 5 characters long.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(FEEDBACK_FILE, "a") as f:
        f.write(f"[{timestamp}] {trainer_name}: {feedback}\n")
    
    print("Feedback sent successfully.")

# ============= LECTURER FUNCTIONS =============
# ONLY functions that lecturers can perform according to assignment

def lecturer_menu(lecturer_name):
    """Lecturer main menu - restricted to lecturer-only functions"""
    while True:
        print(f"\n=== Lecturer Menu - {lecturer_name} ===")
        print("Lecturer Functions:")
        print("1. Register student to module")
        print("2. Update subject enrollment of student")
        print("3. Approve requests from students")
        print("4. Delete students")
        print("5. Update own profile")
        print("6. Logout")
        print("7. Exit")
        
        choice = get_user_input("Enter your choice (1-7): ",
                               lambda x: x in ['1','2','3','4','5','6','7'],
                               "Invalid choice. Please enter 1-7.")
        
        if choice == "1":
            lecturer_register_student()
        elif choice == "2":
            update_student_enrollment()
        elif choice == "3":
            approve_student_requests()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            update_profile(lecturer_name)
        elif choice == "6":
            return
        elif choice == "7":
            sys.exit()

def lecturer_register_student():
    """Lecturer registers student to module"""
    print("\n=== Register Student to Module (Lecturer Only) ===")
    
    student_name = get_user_input("Enter student name: ",
                                 lambda x: len(x) >= 2,
                                 "Student name must be at least 2 characters.")
    
    tp_number = get_user_input("Enter TP number (format: TPxxxxxx): ",
                              lambda x: x.startswith("TP") and len(x) >= 8,
                              "TP number must start with 'TP' and be at least 8 characters.")
    
    email = get_user_input("Enter student email: ",
                          validate_email,
                          "Please enter a valid email address.")
    
    contact = get_user_input("Enter contact number: ",
                           lambda x: x.isdigit() and len(x) >= 10,
                           "Contact number must be at least 10 digits.")
    
    # Display available modules and trainers
    display_available_modules()
    
    module_name = get_user_input("Enter module name: ",
                                lambda x: len(x) >= 2,
                                "Module name must be at least 2 characters.")
    
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    # Find trainer for the module
    trainer_name = get_trainer_for_module(module_name, level)
    if not trainer_name:
        print("No trainer found for this module/level combination.")
        return
    
    address = input("Enter student address: ").strip()
    
    month_of_enrollment = get_user_input("Enter month of enrollment (e.g., January): ",
                                        lambda x: len(x) >= 3,
                                        "Month must be at least 3 characters.")
    
    charges = get_charges_for_module(module_name, level, trainer_name)
    if not charges:
        charges = get_user_input("Enter charges (RM): ",
                               lambda x: x.replace('.', '').isdigit(),
                               "Please enter a valid amount.")
    
    student_id = generate_student_id()
    status = "unpaid"
    
    # Check if student already enrolled in this module
    if is_student_already_enrolled(tp_number, module_name, level):
        print("Student is already enrolled in this module and level.")
        return
    
    with open(STUDENTS_FILE, "a") as f:
        f.write(f"{student_name},{tp_number},{module_name},{level},{trainer_name},{email},{contact},{month_of_enrollment},{charges},{status},{student_id},{address}\n")
    
    print("Student registered successfully by lecturer.")
    print(f"Student ID: {student_id}")

def display_available_modules():
    """Display available modules and trainers"""
    print("\nAvailable modules:")
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            modules = set()
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 3:
                    modules.add(f"{fields[0]} ({fields[2]}) - Trainer: {fields[1]}")
            
            for module in sorted(modules):
                print(f"- {module}")
    except FileNotFoundError:
        print("No modules available.")

def get_trainer_for_module(module_name, level):
    """Get trainer assigned to specific module and level"""
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 3 and fields[0] == module_name and fields[2] == level:
                    return fields[1]
    except FileNotFoundError:
        pass
    return None

def get_charges_for_module(module_name, level, trainer_name):
    """Get charges for specific module, level, and trainer"""
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 4 and fields[0] == module_name and fields[1] == trainer_name and fields[2] == level:
                    return fields[3]
    except FileNotFoundError:
        pass
    return None

def is_student_already_enrolled(tp_number, module_name, level):
    """Check if student is already enrolled in module"""
    try:
        with open(STUDENTS_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 4 and fields[1] == tp_number and fields[2] == module_name and fields[3] == level:
                    return True
    except FileNotFoundError:
        pass
    return False

def update_student_enrollment():
    """Update student's subject enrollment"""
    print("\n=== Update Student Enrollment ===")
    
    tp_number = get_user_input("Enter student TP number: ",
                              lambda x: x.startswith("TP") and len(x) >= 8,
                              "TP number must start with 'TP' and be at least 8 characters.")
    
    # Display current enrollments for student
    display_student_enrollments(tp_number)
    
    current_module = input("Enter current module name: ").strip()
    current_level = get_user_input("Enter current level (Beginner/Intermediate/Advanced): ",
                                  validate_level,
                                  f"Level must be one of: {', '.join(LEVELS)}")
    
    # Display available modules
    display_available_modules()
    
    new_module = input("Enter new module name: ").strip()
    new_level = get_user_input("Enter new level (Beginner/Intermediate/Advanced): ",
                              validate_level,
                              f"Level must be one of: {', '.join(LEVELS)}")
    
    new_trainer = get_trainer_for_module(new_module, new_level)
    if not new_trainer:
        print("No trainer found for this module/level combination.")
        return
    
    try:
        with open(STUDENTS_FILE, "r") as f:
            data = f.readlines()
        
        updated = False
        for i, line in enumerate(data):
            fields = line.strip().split(",")
            if len(fields) >= 4 and fields[1] == tp_number and fields[2] == current_module and fields[3] == current_level:
                fields[2] = new_module
                fields[3] = new_level
                fields[4] = new_trainer
                
                # Update charges if available
                new_charges = get_charges_for_module(new_module, new_level, new_trainer)
                if new_charges and len(fields) >= 9:
                    fields[8] = new_charges
                
                data[i] = ",".join(fields) + "\n"
                updated = True
                break
        
        if updated:
            with open(STUDENTS_FILE, "w") as f:
                f.writelines(data)
            print("Student enrollment updated successfully.")
        else:
            print("Student enrollment record not found.")
            
    except FileNotFoundError:
        print("Students file not found.")

def display_student_enrollments(tp_number):
    """Display current enrollments for a student"""
    print(f"\nCurrent enrollments for {tp_number}:")
    try:
        with open(STUDENTS_FILE, "r") as f:
            found = False
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 4 and fields[1] == tp_number:
                    print(f"- {fields[2]} ({fields[3]}) - Trainer: {fields[4] if len(fields) > 4 else 'TBD'}")
                    found = True
            
            if not found:
                print("No enrollments found for this student.")
    except FileNotFoundError:
        print("Students file not found.")

def approve_student_requests():
    """Approve or reject student requests"""
    print("\n=== Student Requests ===")
    
    try:
        with open(REQUESTS_FILE, "r") as f:
            requests = f.readlines()
    except FileNotFoundError:
        print("No requests file found.")
        return
    
    if not requests:
        print("No pending requests.")
        return
    
    print("Pending requests:")
    print("-" * 60)
    for i, line in enumerate(requests, 1):
        fields = line.strip().split(",")
        if len(fields) >= 4:
            print(f"{i}. Student: {fields[0]}, Module: {fields[1]}, Level: {fields[2]}, Status: {fields[3]}")
    
    try:
        request_num = int(input("\nEnter request number to process (0 to cancel): "))
        if request_num == 0:
            return
        
        if 1 <= request_num <= len(requests):
            selected_request = requests[request_num - 1]
            fields = selected_request.strip().split(",")
            
            print(f"\nProcessing request from {fields[0]} for {fields[1]} ({fields[2]})")
            
            action = get_user_input("Enter action (1=Approve, 2=Reject): ",
                                   lambda x: x in ['1', '2'],
                                   "Please enter 1 for Approve or 2 for Reject.")
            
            if action == '1':
                fields[3] = "approved"
                # Add student to enrollment if approved
                add_approved_student_to_enrollment(fields[0], fields[1], fields[2])
                print("Request approved and student enrolled.")
            else:
                fields[3] = "rejected"
                print("Request rejected.")
            
            requests[request_num - 1] = ",".join(fields) + "\n"
            
            with open(REQUESTS_FILE, "w") as f:
                f.writelines(requests)
                
        else:
            print("Invalid request number.")
            
    except ValueError:
        print("Please enter a valid number.")

def add_approved_student_to_enrollment(student_name, module_name, level):
    """Add approved student to enrollment"""
    trainer_name = get_trainer_for_module(module_name, level)
    charges = get_charges_for_module(module_name, level, trainer_name) or "0"
    
    student_id = generate_student_id()
    
    with open(STUDENTS_FILE, "a") as f:
        f.write(f"{student_name},TBD,{module_name},{level},{trainer_name},TBD,TBD,TBD,{charges},unpaid,{student_id},TBD\n")

def delete_student():
    """Delete completed students"""
    print("\n=== Delete Student ===")
    
    tp_number = get_user_input("Enter student TP number to delete: ",
                              lambda x: len(x) >= 6,
                              "TP number must be at least 6 characters.")
    
    try:
        with open(STUDENTS_FILE, "r") as f:
            students = f.readlines()
    except FileNotFoundError:
        print("Students file not found.")
        return
    
    # Find and display student info
    student_found = False
    for line in students:
        fields = line.strip().split(",")
        if len(fields) >= 2 and fields[1] == tp_number:
            print(f"\nStudent found: {fields[0]} ({fields[1]})")
            print(f"Modules: {fields[2] if len(fields) > 2 else 'N/A'}")
            student_found = True
            break
    
    if not student_found:
        print("Student not found.")
        return
    
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    
    if confirm == 'y':
        filtered_students = []
        for line in students:
            fields = line.strip().split(",")
            if not (len(fields) >= 2 and fields[1] == tp_number):
                filtered_students.append(line)
        
        with open(STUDENTS_FILE, "w") as f:
            f.writelines(filtered_students)
        
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")

# ============= STUDENT FUNCTIONS =============
# ONLY functions that students can perform according to assignment

def student_menu(student_name):
    """Student main menu - restricted to student-only functions"""
    while True:
        print(f"\n=== Student Menu - {student_name} ===")
        print("Student Functions:")
        print("1. View schedule of coaching classes")
        print("2. Send request to enroll in additional coaching class")
        print("3. Delete pending request")
        print("4. View invoice and make payment")
        print("5. Update own profile")
        print("6. Logout")
        print("7. Exit")
        
        choice = get_user_input("Enter your choice (1-7): ",
                               lambda x: x in ['1','2','3','4','5','6','7'],
                               "Invalid choice. Please enter 1-7.")
        
        if choice == "1":
            view_student_schedule(student_name)
        elif choice == "2":
            send_enrollment_request(student_name)
        elif choice == "3":
            delete_pending_request(student_name)
        elif choice == "4":
            view_invoice_and_pay(student_name)
        elif choice == "5":
            update_profile(student_name)
        elif choice == "6":
            return
        elif choice == "7":
            sys.exit()

def view_student_schedule(student_name):
    """View student's coaching class schedule"""
    print(f"\n=== Class Schedule for {student_name} ===")
    
    try:
        with open(STUDENTS_FILE, "r") as f:
            found = False
            print("-" * 80)
            print(f"{'Module':<15} {'Level':<12} {'Trainer':<15} {'Schedule':<20} {'Status'}")
            print("-" * 80)
            
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 10 and fields[0] == student_name and fields[9] == "paid":
                    module_name = fields[2]
                    level = fields[3]
                    trainer_name = fields[4]
                    
                    # Get schedule from trainer modules
                    schedule = get_schedule_for_module(module_name, level, trainer_name)
                    
                    print(f"{module_name:<15} {level:<12} {trainer_name:<15} {schedule:<20} {fields[9]}")
                    found = True
            
            if not found:
                print("No paid coaching classes found. Please make payment to view schedules.")
                
    except FileNotFoundError:
        print("Students file not found.")

def get_schedule_for_module(module_name, level, trainer_name):
    """Get schedule for specific module"""
    try:
        with open(TRAINER_MODULES_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 5 and fields[0] == module_name and fields[1] == trainer_name and fields[2] == level:
                    return fields[4] if fields[4] != "TBD" else "Schedule TBD"
    except FileNotFoundError:
        pass
    return "Schedule TBD"

def send_enrollment_request(student_name):
    """Send request to enroll in additional coaching class"""
    print("\n=== Send Enrollment Request ===")
    
    # Display available modules
    display_available_modules()
    
    module = get_user_input("Enter module name for additional coaching: ",
                           lambda x: len(x) >= 2,
                           "Module name must be at least 2 characters.")
    
    level = get_user_input("Enter level (Beginner/Intermediate/Advanced): ",
                          validate_level,
                          f"Level must be one of: {', '.join(LEVELS)}")
    
    # Check if request already exists
    if is_request_already_sent(student_name, module, level):
        print("You have already sent a request for this module and level.")
        return
    
    status = "pending"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(REQUESTS_FILE, "a") as f:
        f.write(f"{student_name},{module},{level},{status},{timestamp}\n")
    
    print("Enrollment request sent successfully.")

def is_request_already_sent(student_name, module, level):
    """Check if request already exists"""
    try:
        with open(REQUESTS_FILE, "r") as f:
            for line in f:
                fields = line.strip().split(",")
                if len(fields) >= 4 and fields[0] == student_name and fields[1] == module and fields[2] == level and fields[3] == "pending":
                    return True
    except FileNotFoundError:
        pass
    return False

def delete_pending_request(student_name):
    """Delete pending enrollment request"""
    print(f"\n=== Delete Pending Request - {student_name} ===")
    
    try:
        with open(REQUESTS_FILE, "r") as f:
            requests = f.readlines()
    except FileNotFoundError:
        print("No requests found.")
        return
    
    # Display student's pending requests
    student_requests = []
    print("Your pending requests:")
    print("-" * 50)
    
    for i, line in enumerate(requests):
        fields = line.strip().split(",")
        if len(fields) >= 4 and fields[0] == student_name and fields[3] == "pending":
            student_requests.append((i, line))
            print(f"{len(student_requests)}. {fields[1]} ({fields[2]})")
    
    if not student_requests:
        print("No pending requests found.")
        return
    
    try:
        request_num = int(input("\nEnter request number to delete (0 to cancel): "))
        if request_num == 0:
            return
        
        if 1 <= request_num <= len(student_requests):
            original_index = student_requests[request_num - 1][0]
            requests.pop(original_index)
            
            with open(REQUESTS_FILE, "w") as f:
                f.writelines(requests)
            
            print("Request deleted successfully.")
        else:
            print("Invalid request number.")
            
    except ValueError:
        print("Please enter a valid number.")

def view_invoice_and_pay(student_name):
    """View invoice and make payment"""
    print(f"\n=== Invoice for {student_name} ===")
    
    try:
        with open(STUDENTS_FILE, "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        print("Students file not found.")
        return
    
    total_charges = 0.0
    unpaid_modules = []
    
    print("-" * 70)
    print(f"{'Module':<15} {'Level':<12} {'Trainer':<15} {'Charges':<10} {'Status'}")
    print("-" * 70)
    
    for i, line in enumerate(data):
        fields = line.strip().split(",")
        if len(fields) >= 10 and fields[0] == student_name:
            charges = float(fields[8]) if fields[8].replace('.', '').isdigit() else 0.0
            print(f"{fields[2]:<15} {fields[3]:<12} {fields[4]:<15} RM{charges:<8.2f} {fields[9]}")
            
            if fields[9] == "unpaid":
                total_charges += charges
                unpaid_modules.append(i)
    
    if total_charges == 0:
        print("\nNo outstanding payments.")
        return
    
    print("-" * 70)
    print(f"Total Outstanding: RM{total_charges:.2f}")
    
    pay_option = input("\nDo you want to make payment now? (y/n): ").strip().lower()
    
    if pay_option == 'y':
        print("\n=== PAYMENT INVOICE ===")
        print(f"Bank: Maybank")
        print(f"Receiver: APU Programming Café")
        print(f"Sender: {student_name}")
        print(f"Amount: RM{total_charges:.2f}")
        print("=" * 25)
        
        confirm_payment = input("\nConfirm payment? (y/n): ").strip().lower()
        
        if confirm_payment == 'y':
            # Update payment status
            for index in unpaid_modules:
                fields = data[index].strip().split(",")
                if len(fields) >= 10:
                    fields[9] = "paid"
                    data[index] = ",".join(fields) + "\n"
            
            with open(STUDENTS_FILE, "w") as f:
                f.writelines(data)
            
            print("Payment successful! Thank you.")
            print("You can now view your class schedules.")
        else:
            print("Payment cancelled.")
    else:
        print("Payment cancelled.")

# ============= MAIN FUNCTION =============

if __name__ == "__main__":
    main_menu()