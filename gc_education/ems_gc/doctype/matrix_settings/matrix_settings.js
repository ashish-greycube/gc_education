// Copyright (c) 2024, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Matrix Settings", {
    refresh(frm) {
        frm.add_custom_button(__("Sync Attendance"), function () {
            frappe.call({
                method: 'gc_education.ems_gc.controllers.attendance.sync_user_attendance_events',
                freeze: true,
                freeze_message: __("Please wait while the attendance is synced."),
                callback: function (r) {
                    console.log(r);

                    frm.refresh();
                }
            });
        });
    },
});
