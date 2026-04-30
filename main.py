import sqlite3
import re

DB_NAME = "students.db"

# --- DATABASE SETUP ---
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            middle_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            place_of_birth TEXT NOT NULL,
            email_address TEXT UNIQUE NOT NULL,
            contact_number TEXT NOT NULL,
            section TEXT NOT NULL,
            league_color TEXT NOT NULL
        )
    """)
    return conn

# --- VALIDATION HELPERS ---
def is_valid_text(text):
    return bool(text and re.match(r"^[A-Za-z\s]+$", text))

# --- ADD STUDENT FUNCTION ---
def add_student():
    print("\n" + "="*40)
    print("      PSHS STUDENT REGISTRATION")
    print("="*40)
    print("(Type 'EXIT' at any prompt to cancel)")

    while True:
        sid = input("ID (20YY-XXX): ").strip()
        if sid.upper() == 'EXIT': return
        if re.match(r"^20\d{2}-\d{3}$", sid):
            student_id = sid
            break
        print(">> Error: ID must be 20YY-XXX.")

    while True:
        f_name = input("First Name: ").strip()
        m_name = input("Middle Name: ").strip()
        l_name = input("Last Name: ").strip()
        if 'EXIT' in [f_name.upper(), m_name.upper(), l_name.upper()]: return
        if is_valid_text(f_name) and is_valid_text(l_name):
            break
        print(">> Error: First and Last names are required (letters only).")

    while True:
        val = input("Gender (Male/Female/Others - specify): ").strip()
        if val.upper() == 'EXIT': return
        if val in ["Male", "MALE", "Female", "FEMALE"] or val.lower().startswith("others"):
            gender = val
            break
        print(">> Error: Use 'Male', 'Female', or 'Others - [detail]'.")

    while True:
        val = input("Birth Date (MM/DD/YYYY): ").strip()
        if val.upper() == 'EXIT': return
        if re.match(r"^\d{2}/\d{2}/\d{4}$", val):
            birthdate = val
            break
        print(">> Error: Use MM/DD/YYYY format.")

    pob = input("Place of Birth: ").strip()

    while True:
        val = input("Email (@cmc.pshs.edu.ph): ").strip()
        if val.upper() == 'EXIT': return
        if val.lower().endswith("@cmc.pshs.edu.ph"):
            email = val
            break
        print(">> Error: Must end with @cmc.pshs.edu.ph.")

    while True:
        val = input("Contact (+639 or 09...): ").strip()
        if val.upper() == 'EXIT': return
        if re.match(r"^(\+639|09)\d{9}$", val):
            contact = val
            break
        print(">> Error: Use +639 or 09 followed by 9 digits.")

    sections = ["Dahlia", "Kamia", "Rosal", "Sampaguita"]
    while True:
        val = input(f"Section ({'/'.join(sections)}): ").strip()
        if val.upper() == 'EXIT': return
        if val in sections:
            section = val
            break
        print(f">> Error: Must be one of {sections}.")

    colors = ["Red", "Yellow", "Green", "Blue"]
    while True:
        val = input(f"League Color ({'/'.join(colors)}): ").strip()
        if val.upper() == 'EXIT': return
        if val in colors:
            league_color = val
            break
        print(f">> Error: Must be one of {colors}.")

    try:
        conn = connect_db()
        query = """INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
        conn.execute(query, (student_id, f_name, m_name, l_name, gender, birthdate, pob, email, contact, section, league_color))
        conn.commit()
        print("\n[SUCCESS] Record added!")
    except sqlite3.IntegrityError:
        print("\n[ERROR] ID or Email already exists.")
    finally:
        conn.close()

# --- VIEW FUNCTION ---
def view_students():
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("\nNo records found.")
        return

    print("\n--- Student List ---")
    print("-" * 120)
    for r in rows:
        print(f"ID: {r[0]} | First Name: {r[1]} | Middle Name: {r[2]} | Last Name: {r[3]} | Gender: {r[4]} | Birth Date: {r[5]} | Place of Birth: {r[6]} | Email Address: {r[7]} | Contact: {r[8]} | Section: {r[9]} | Color: {r[10]}")
    print("-" * 120)

# --- UPDATE FUNCTION ---
def update_student():
    student_id = input("Enter Student ID to update (20YY-XXX): ").strip()
    
    conn = connect_db()
    cursor = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return print("Error: Student ID not found.")

    print(f"\n--- Updating Student ID: {student_id} ---")
    
    # Use same validation logic as Add
    f_name = input("New First Name: ").strip()
    l_name = input("New Last Name: ").strip()
    # (Note: For brevity, you can add more fields here following the Add Student patterns)

    if is_valid_text(f_name) and is_valid_text(l_name):
        conn.execute("UPDATE students SET first_name = ?, last_name = ? WHERE id = ?", (f_name, l_name, student_id))
        conn.commit()
        print("Update successful.")
    else:
        print("Update failed: Invalid names.")
    conn.close()

# --- DELETE FUNCTION ---
def delete_student():
    student_id = input("Enter Student ID to delete (20YY-XXX): ").strip()
    conn = connect_db()
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        print("Error: Student ID not found.")
    else:
        print("Student deleted successfully.")
    conn.close()

# --- MAIN MENU LOOP ---
while True:
    print("""
==== STUDENT DATABASE SYSTEM ====
1. Add Student
2. View Students
3. Update Student
4. Delete Student
5. Exit
=================================
""")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        print("Terminating...")
        break
    else:
        print("Invalid choice. Please try again.")