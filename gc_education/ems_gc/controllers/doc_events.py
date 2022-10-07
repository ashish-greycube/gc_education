# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe


def validate_student_applicant(doc, method):
    for d in ["Father", "Mother"]:
        if [x for x in doc.guardians if x.relation == d]:
            continue

        relation = frappe.scrub(d)
        guardian = frappe.get_doc(
            {
                "doctype": "Guardian",
                "designation": "Father",
                "annual_income": doc.get(f"{relation}_annual_income_cf"),
                "education": doc.get(f"{relation}_education_cf"),
                "email_address": doc.get(f"{relation}_mail_cf"),
                "mobile_number": doc.get(f"{relation}_mobile_cf"),
                "guardian_name": doc.get(f"{relation}_name_cf"),
                "name_of_firm": doc.get(f"{relation}_name_of_firm_cf"),
                "occupation": doc.get(f"{relation}_occupation_cf"),
            }
        ).insert()

        doc.append(
            "guardians",
            {
                "guardian": guardian.name,
                "guardian_name": guardian.guardian_name,
                "relation": d,
            },
        )
