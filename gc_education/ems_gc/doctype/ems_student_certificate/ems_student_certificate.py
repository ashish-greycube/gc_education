# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


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

        student_doc = frappe.get_doc("Student", self.student)

        if not self.birth_place:
            self.birth_place = student_doc.birth_place
        if not self.state:
            self.state = student_doc.birth_state
        if not self.caste:
            self.caste = student_doc.caste
        if not self.student_group_name and self.student_group:
            self.student_group_name = self.student_group.split("/")[0]
