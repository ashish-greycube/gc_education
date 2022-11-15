# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from gc_education.ems_gc.report.student_class_list.student_class_list import (
    execute as class_list,
)
from frappe.utils import strip_html_tags, cint
from education.education.doctype.student_attendance.student_attendance import (
    get_holiday_list,
)


class EMSStudentCertificate(Document):
    def validate(self):
        guardians = frappe.db.sql(
            """
        select guardian_name , relation
        from `tabStudent Guardian` tsg
        where tsg.parent = %s
        """,
            (self.student),
            as_dict=True,
        )

        for d in guardians:
            if d.relation == "Father":
                self.fathers_name = d.guardian_name
            if d.relation == "Mother":
                self.mothers_name = d.guardian_name

        if not self.guardian_name:
            self.guardian_name = (
                self.fathers_name
                or self.mothers_name
                or guardians
                and guardians[0].guardian_name
            )

        student_doc = frappe.db.get_value(
            "Student",
            self.student,
            ["birth_place", "birth_state", "caste", "caste_category", "gender"],
            as_dict=1,
        )

        def set_if_blank(field, value):
            if not self.get(field):
                self.update({field: value})

        set_if_blank("birth_place", student_doc.birth_place)
        set_if_blank("state", student_doc.birth_state)
        set_if_blank("caste", student_doc.caste)
        set_if_blank("category", student_doc.caste_category)

        self.set("title", "Kumar" if student_doc.gender == "Male" else "Kumari")

        _, data = class_list(
            filters=frappe._dict(
                {
                    "academic_year": self.academic_year,
                    "academic_term": self.academic_term,
                    "student": self.student,
                    "as_on_date": frappe.utils.today(),
                }
            )
        )

        for d in data:
            if d.get("program"):
                set_if_blank("program", d.program)
                set_if_blank("student_group", d.student_group)
                set_if_blank("student_group_name", d.student_group.split("/")[0])

                for course in frappe.db.sql(
                    """
                    select 
                        GROUP_CONCAT(course SEPARATOR ', ') course  
                    from `tabCourse Enrollment` tce 
                    where student = %s and program_enrollment = %s
                """,
                    (self.student, d.program_enrollment),
                ):
                    set_if_blank("course_enrollment", course[0])

                activities = []
                for log in frappe.db.get_all(
                    "Student Log",
                    {
                        "academic_year": self.academic_year,
                        "academic_term": self.academic_term,
                        "student": self.student,
                    },
                    ["log"],
                ):
                    activities.append(strip_html_tags(log.log))

                set_if_blank("student_activities", "\n".join(activities))

        # attendance
        holidays = frappe.db.get_value(
            "Holiday List", get_holiday_list(), ["total_holidays"]
        )
        for d in frappe.db.sql(
            """
        	select count(*) `count` , 
            DATEDIFF(tay.year_end_date, tay.year_start_date) + 1 
            from `tabStudent Attendance` tsa
            inner join `tabAcademic Year` tay on tay.year_start_date <= tsa.`date` 
            and tay.year_end_date >= tsa.date and tay.name = %s
            where tsa.docstatus = 1 and tsa.status = 'Present' and tsa.student = %s
        """,
            (self.academic_year, self.student),
        ):
            set_if_blank("student_attendance_days_in_a_year", cint(d[0]))
            set_if_blank("total_attendance_days_in_a_year", cint(d[1]) - holidays)
