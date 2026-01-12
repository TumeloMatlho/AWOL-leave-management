# import flet as ft
# from Awol import (
#     authenticate,
#     get_leave_status,
#     apply_leave,
#     get_all_employees,
#     get_all_leave_balances,
#     reset_leave,
# )

# def main(page: ft.Page):
#     page.title = "AWOL Leave Management System"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.window_width = 500
#     page.window_height = 400
#     page.window_resizable = True
#     page.theme_mode = "light"

#     def show_login():
#         page.clean()
#         username = ft.TextField(label="Employee ID", width=300)
#         password = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
#         status = ft.Text("")

#         def login_click(e):
#             try:
#                 user_id = int(username.value)
#             except ValueError:
#                 status.value = "Employee ID is invalid"
#                 page.update()
#                 return

#             user = authenticate(user_id, password.value)
#             if user:
#                 show_dashboard(user)
#             else:
#                 status.value = "Invalid username or password"
#                 page.update()

#         login_btn = ft.ElevatedButton("Login", on_click=login_click)
#         page.add(ft.Column([username, password, login_btn, status], alignment="center"))

#     def show_dashboard(user):
#         page.clean()
#         emp_id, name, _, total_leave, leave_taken, role = user
#         remaining = total_leave - leave_taken

#         welcome = ft.Text(f"Welcome {name} ({role})", size=20, weight="bold")
#         balance = ft.Text(f"Leave balance: {remaining}/{total_leave}")
#         status_text = ft.Text("")

#         def logout(e):
#             show_login()

#         logout_btn = ft.ElevatedButton("Logout", on_click=logout)

#         controls = [welcome, balance]  # Start with common items

#         # -------- Employee-only Actions --------
#         if role == "employee":
#             def apply_leave_click(e):
#                 days_input = ft.TextField(label="Days", width=100)
#                 status_apply = ft.Text("")

#                 def confirm_apply(ev):
#                     try:
#                         days = int(days_input.value)
#                     except ValueError:
#                         status_apply.value = "Please enter a valid number."
#                         page.update()
#                         return
#                     success, msg = apply_leave(emp_id, days)
#                     status_apply.value = msg
#                     if success:
#                         refreshed = get_leave_status(emp_id)
#                         balance.value = f"Leave balance: {refreshed['remaining']}/{refreshed['total']}"
#                     dlg.open = False
#                     status_text.value = msg
#                     page.update()

#                 confirm_btn = ft.ElevatedButton("Confirm", on_click=confirm_apply)
#                 dlg = ft.AlertDialog(
#                     title=ft.Text("Apply for Leave"),
#                     content=ft.Column([days_input, status_apply]),
#                     actions=[confirm_btn]
#                 )
#                 page.open(dlg)
#                 page.update()

#             def view_status_click(e):
#                 try:
#                     refreshed = get_leave_status(emp_id)
#                     if refreshed:
#                         status_text.value = (
#                             f"Taken: {refreshed['taken']} / {refreshed['total']} | Remaining: {refreshed['remaining']}"
#                         )
#                     else:
#                         status_text.value = "Error fetching leave status."
#                 except Exception as ex:
#                     status_text.value = f"Error: {ex}"
#                 page.update()

#             controls += [
#                 ft.ElevatedButton("Apply for Leave", on_click=apply_leave_click),
#                 ft.ElevatedButton("View Leave Status", on_click=view_status_click),
#             ]

#         # -------- Manager-only Actions --------
#         elif role == "manager":
#             def view_all_employees(e):
#                 try:
#                     rows = get_all_employees()
#                     if rows:
#                         content = "\n".join([f"ID: {r[0]} | Name: {r[1]} | Role: {r[2]}" for r in rows])
#                         # content = rows[0]
#                         # print(content)
#                     else:
#                         content = "No employees found."
#                 except Exception as ex:
#                     content = f"Error: {ex}"
#                 dlg = ft.AlertDialog(
#                     title=ft.Text("All Employees"),
#                     content=ft.Text(content)
#                 )
#                 page.open(dlg)
#                 page.update()

#             def view_balances(e):
#                 try:
#                     rows = get_all_leave_balances()
#                     if rows:
#                         content = "\n".join([f"ID: {r[0]} | {r[1]} | Remaining: {r[2]-r[3]} days" for r in rows])
#                     else:
#                         content = "No leave balances found."
#                 except Exception as ex:
#                     content = f"Error: {ex}"
#                 dlg = ft.AlertDialog(
#                     title=ft.Text("Leave Balances"),
#                     content=ft.Text(content)
#                 )
#                 page.open(dlg)
#                 page.update()

#             def reset_leave_click(e):
#                 emp_input = ft.TextField(label="Employee ID", width=150)
#                 status_reset = ft.Text("")

#                 def confirm_reset(ev):
#                     try:
#                         emp = int(emp_input.value)
#                         success, msg = reset_leave(emp)
#                         status_reset.value = msg
#                         status_text.value = msg
#                     except ValueError:
#                         status_reset.value = "Invalid ID."
#                         status_text.value = "Invalid ID."
#                     dialog.open = False
#                     page.update()

#                 confirm_btn = ft.ElevatedButton("Confirm", on_click=confirm_reset)
#                 dlg = ft.AlertDialog(
#                     title=ft.Text("Reset Employee Leave"),
#                     content=ft.Column([emp_input, status_reset]),
#                     actions=[confirm_btn]
#                 )
#                 page.open(dlg)
#                 page.update()

#             controls += [
#                 ft.ElevatedButton("View All Employees", on_click=view_all_employees),
#                 ft.ElevatedButton("View Leave Balances", on_click=view_balances),
#                 ft.ElevatedButton("Reset Employee Leave", on_click=reset_leave_click),
#             ]

#         controls += [logout_btn, status_text]  # Add logout and status at the bottom

#         page.add(ft.Column(controls, spacing=20, horizontal_alignment="center"))

#     show_login()

# ft.app(target=main)

import flet as ft
import httpx

API_URL = "http://127.0.0.1:8000"   # FastAPI server base URL

def main(page: ft.Page):
    page.title = "AWOL Leave Management System"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 400
    page.window_resizable = True
    page.theme_mode = "light"

    client = httpx.Client()

    # ------------------- LOGIN SCREEN -------------------
    def show_login():
        page.clean()
        username = ft.TextField(label="Employee ID", width=300)
        password = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
        status = ft.Text("")

        def login_click(e):
            try:
                user_id = int(username.value)
            except ValueError:
                status.value = "Employee ID is invalid"
                page.update()
                return

            try:
                r = client.post(f"{API_URL}/login", params={"employee_id": user_id, "password": password.value})
                if r.status_code == 200:
                    show_dashboard(r.json())
                else:
                    status.value = r.json().get("detail", "Login failed")
            except Exception as ex:
                status.value = f"Error: {ex}"
            page.update()

        login_btn = ft.ElevatedButton("Login", on_click=login_click)
        page.add(ft.Column([username, password, login_btn, status], alignment="center"))

    # ------------------- DASHBOARD -------------------
    def show_dashboard(user):
        page.clean()
        emp_id, name, total_leave, leave_taken, role = (
            user["employee_id"], user["name"], user["total_leave"], user["leave_taken"], user["role"]
        )
        remaining = total_leave - leave_taken

        welcome = ft.Text(f"Welcome {name} ({role})", size=20, weight="bold")
        balance = ft.Text(f"Leave balance: {remaining}/{total_leave}")
        status_text = ft.Text("")

        def logout(e):
            show_login()

        logout_btn = ft.ElevatedButton("Logout", on_click=logout)
        controls = [welcome, balance]

        # -------- Employee Actions --------
        if role == "employee":
            def apply_leave_click(e):
                days_input = ft.TextField(label="Days", width=100)
                status_apply = ft.Text("")

                def confirm_apply(ev):
                    try:
                        days = int(days_input.value)
                        r = client.post(f"{API_URL}/apply_leave", params={"employee_id": emp_id, "days": days})
                        if r.status_code == 200:
                            msg = r.json()["message"]
                            refreshed = client.get(f"{API_URL}/leave_status/{emp_id}").json()
                            balance.value = f"Leave balance: {refreshed['remaining']}/{refreshed['total']}"
                        else:
                            msg = r.json().get("detail", "Error applying leave")
                        status_apply.value = msg
                        status_text.value = msg
                        dlg.open = False
                        page.update()
                    except Exception as ex:
                        status_apply.value = f"Error: {ex}"
                        page.update()

                confirm_btn = ft.ElevatedButton("Confirm", on_click=confirm_apply)
                dlg = ft.AlertDialog(
                    title=ft.Text("Apply for Leave"),
                    content=ft.Column([days_input, status_apply]),
                    actions=[confirm_btn]
                )
                page.open(dlg)

            def view_status_click(e):
                try:
                    r = client.get(f"{API_URL}/leave_status/{emp_id}")
                    if r.status_code == 200:
                        refreshed = r.json()
                        status_text.value = (
                            f"Taken: {refreshed['taken']} / {refreshed['total']} | Remaining: {refreshed['remaining']}"
                        )
                    else:
                        status_text.value = "Error fetching leave status"
                except Exception as ex:
                    status_text.value = f"Error: {ex}"
                page.update()

            controls += [
                ft.ElevatedButton("Apply for Leave", on_click=apply_leave_click),
                ft.ElevatedButton("View Leave Status", on_click=view_status_click),
            ]

        # -------- Manager Actions --------
        elif role == "manager":
            def view_all_employees(e):
                try:
                    r = client.get(f"{API_URL}/employees")
                    if r.status_code == 200:
                        rows = r.json()
                        content = "\n".join([f"ID: {r[0]} | Name: {r[1]} | Role: {r[2]}" for r in rows])
                    else:
                        content = "Error fetching employees"
                except Exception as ex:
                    content = f"Error: {ex}"
                dlg = ft.AlertDialog(title=ft.Text("All Employees"), content=ft.Text(content))
                page.open(dlg)

            def view_balances(e):
                try:
                    r = client.get(f"{API_URL}/leave_balances")
                    if r.status_code == 200:
                        rows = r.json()
                        content = "\n".join([f"ID: {r[0]} | {r[1]} | Remaining: {r[2]-r[3]} days" for r in rows])
                    else:
                        content = "Error fetching balances"
                except Exception as ex:
                    content = f"Error: {ex}"
                dlg = ft.AlertDialog(title=ft.Text("Leave Balances"), content=ft.Text(content))
                page.open(dlg)

            def reset_leave_click(e):
                emp_input = ft.TextField(label="Employee ID", width=150)
                status_reset = ft.Text("")

                def confirm_reset(ev):
                    try:
                        emp = int(emp_input.value)
                        r = client.post(f"{API_URL}/reset_leave", params={"employee_id": emp})
                        msg = r.json().get("message", r.json().get("detail", "Error"))
                        status_reset.value = msg
                        status_text.value = msg
                        dlg.open = False
                        page.update()
                    except Exception:
                        status_reset.value = "Invalid ID."
                        page.update()

                confirm_btn = ft.ElevatedButton("Confirm", on_click=confirm_reset)
                dlg = ft.AlertDialog(
                    title=ft.Text("Reset Employee Leave"),
                    content=ft.Column([emp_input, status_reset]),
                    actions=[confirm_btn]
                )
                page.open(dlg)

            controls += [
                ft.ElevatedButton("View All Employees", on_click=view_all_employees),
                ft.ElevatedButton("View Leave Balances", on_click=view_balances),
                ft.ElevatedButton("Reset Employee Leave", on_click=reset_leave_click),
            ]

        controls += [logout_btn, status_text]
        page.add(ft.Column(controls, spacing=20, horizontal_alignment="center"))

    show_login()

ft.app(target=main)


