import frappe
import pymssql
from frappe.utils import add_days, getdate, now, cint

# e.g. check out has to be 30 minutes after check in
MINIMUM_CHECK_OUT_DELAY_MINUTES = 30


def get_matrix_connection():
    settings = frappe.get_doc("Matrix Settings", "Matrix Settings")
    try:
        return pymssql.connect(
            host=settings.host,
            port=settings.port,
            database=settings.database,
            user=settings.user,
            password=settings.password,
            login_timeout=5,
            timeout=5,
            tds_version="7.0",
        )
    except Exception as ex:
        print(frappe.get_traceback())
        frappe.log_error(
            title="Matrix Connection Error", message=frappe.get_traceback()
        )


def make_checkin(row, employee, in_out):
    try:
        frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": employee,
                "log_type": in_out,
                "time": in_out == "IN" and row["check_in"] or row["check_out"],
                "skip_auto_attendance": 0,
            }
        ).insert(ignore_permissions=True)
    except frappe.ValidationError:
        pass


@frappe.whitelist()
def sync_user_attendance_events():
    if not cint(frappe.db.get_single_value("Matrix Settings", "enable_sync")):
        frappe.throw("Attendance Sync is disabled")

    sync_date = add_days(
        frappe.db.get_single_value("Matrix Settings", "last_sync_date"), 1
    )

    employees = {
        d.employee_number: d.name
        for d in frappe.db.sql(
            """ select name , employee_number from tabEmployee """,
            as_dict=True,
        )
    }

    connection = get_matrix_connection()

    if not connection:
        frappe.msgprint("Could not connect to Matrix. Please try later.")

    cursor = connection.cursor(as_dict=True)
    cursor.execute(
        """
        SELECT  UserID , UserName , Edate , min(EventDateTime) check_in , max(EventDateTime) check_out ,
        DATEDIFF(MINUTE,  min(EventDateTime) ,  max(EventDateTime)) after_minutes
        from Mx_VEW_UserAttendanceEvents
        where IDateTime > %s
        group by UserID , UserName , Edate
        order by UserName 
    """,
        (sync_date,),
    )
    row = cursor.fetchone()
    while row:
        if employee := employees.get(row["UserID"]):
            print(row["check_in"], row["check_out"], row["after_minutes"])
            make_checkin(row, employee, "IN")
            if row["after_minutes"] > MINIMUM_CHECK_OUT_DELAY_MINUTES:
                make_checkin(row, employee, "OUT")
        row = cursor.fetchone()

    frappe.db.set_value("Matrix Settings", "Matrix Settings", "last_sync_date", now())

    frappe.db.commit()
