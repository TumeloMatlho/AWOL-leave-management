# 🕒 AWOL Leave Management System

A desktop-based **Leave Management System** built with [Flet](https://flet.dev) (Python GUI framework) and **SQLite3** for local data storage.  
The system allows employees to **apply for leave**, **view leave balances**, and **track leave status**, while managers can **view all employees**, **check leave balances**, and **reset leave records**.

---

## 🚀 Features

### 👤 Employee
- Login securely with hashed credentials.
- View remaining leave balance.
- Apply for leave directly through the system.
- View leave status (taken vs total).
- Logout anytime.

### 🧑‍💼 Manager
- Login with manager credentials.
- View all registered employees.
- View employees’ leave balances.
- Reset an employee’s leave.
- Logout after session.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-------------|----------|
| **Python** | Core programming language |
| **Flet** | GUI framework for building desktop apps |
| **SQLite3** | Local database for persistent data storage |
| **Hashlib** | Password encryption for secure login |

---

# How to run code
1. **Create a virtual environment**

    python -m venv 

    venv\Scripts\activate 

2. **Install dependencies**

    pip install flet 

    no need to install SQLite as it is built-in with Python 

    pip install fastapi 

3. **Run the program**

    python AWOL.py 

    python AWOLGUI.py 

    python AWOLAPI.py 

👨‍💻 Author:

GROUP 09

📅 Created: 29 October 2025

