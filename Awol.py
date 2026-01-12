import sqlite3
import hashlib

# --- DB Setup ---
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# connect to the database
conn = sqlite3.connect('awol.db', check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS awol (
          employee_id INTEGER PRIMARY KEY,
          employee_name TEXT,
          employee_password TEXT,
          total_leave INTEGER,
          leave_taken INTEGER,
          role TEXT
     )""")

# ---------------- AUTHENTICATION ----------------
def authenticate(username, password):
    try:
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM awol WHERE employee_id=? AND employee_password=?", (username, hashed_password))
        user = c.fetchone()
        if user:
            return user  # tuple: (employee_id, name, password, total_leave, leave_taken, role)
        else:
            return None
    except Exception as e:
        return None

# ---------------- EMPLOYEE FUNCTIONS ----------------
def get_leave_status(employee_id):
    try:
        c.execute("SELECT total_leave, leave_taken FROM awol WHERE employee_id=?", (employee_id,))
        row = c.fetchone()
        if row:
            total, taken = row
            return {"total": total, "taken": taken, "remaining": total - taken}
        return None
    except Exception as e:
        return None

def apply_leave(employee_id, days):
    try:
        c.execute("SELECT total_leave, leave_taken FROM awol WHERE employee_id=?", (employee_id,))
        row = c.fetchone()
        if not row:
            return False, "Employee not found."

        total, taken = row
        remaining = total - taken

        if days <= 0:
            return False, "Invalid number of days."
        if days > remaining:
            return False, f"Not enough leave days available. You have {remaining} days remaining."

        new_taken = taken + days
        c.execute("UPDATE awol SET leave_taken=? WHERE employee_id=?", (new_taken, employee_id))
        conn.commit()
        return True, f"Leave approved. Remaining: {total - new_taken} days."
    except Exception as e:
        return False, f"Error applying leave. Please try again."

# ---------------- MANAGER FUNCTIONS ----------------
def get_all_employees():
    try:
        c.execute("SELECT employee_id, employee_name, role FROM awol")
        rows = c.fetchall()
        return rows
    except Exception as e:
        return []

def get_all_leave_balances():
    try:
        c.execute("SELECT employee_id, employee_name, total_leave, leave_taken FROM awol WHERE role='employee'")
        rows = c.fetchall()
        return rows
    except Exception as e:
        return []

def reset_leave(employee_id):
    try:
        c.execute("SELECT role FROM awol WHERE employee_id=?", (employee_id,))
        employee = c.fetchone()

        if not employee:
            return False, "Employee not found."

        if employee[0] == 'manager':
            return False, "Cannot reset leave for managers."

        c.execute("UPDATE awol SET leave_taken=0 WHERE employee_id=?", (employee_id,))
        conn.commit()

        return True, f"Leave successfully reset for employee ID {employee_id}"
    except Exception as e:
        return False, "Error resetting leave. Please try again."

