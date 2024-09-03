## GC Education

Education Module Extensions

#### Sync Attendance with Matrix

- Attendance is synced from on-premise MSSQL instance in the school. (view Mx_VEW_UserAttendanceEvents)
- An Employee CheckIn is created in ERP for first event (IN) and last event (OUT) per user for the day
- A cron is scheduled to run at 1800, to sync attendance since last sync
- User can manually trigger a sync since any date from Matrix Settings by changing the Last Sync Date
- Matrix Settings has the last sync date, which is the date after which all events are fetched from Matrix
- Attendance will have to be created in Erp through Auto Attendance 
- Syncing feature can be disabled from Matrix Settings
- NOTE: The PC with the SQL INSTANCE is switched off after 6 PM ususally.


#### License

MIT

<hr>

#### Contact Us  

<a href="https://greycube.in"><img src="https://greycube.in/files/greycube_logo09eade.jpg" width="250" height="auto"></a> <br>
1<sup>st</sup> ERPNext [Certified Partner](https://frappe.io/api/method/frappe.utils.print_format.download_pdf?doctype=Certification&name=PARTCRTF00002&format=Partner%20Certificate&no_letterhead=0&letterhead=Blank&settings=%7B%7D&_lang=en#toolbar=0)
<sub> <img src="https://greycube.in/files/certificate.svg" width="20" height="20"> </sub>
& winner of the [Best Partner Award](https://frappe.io/partners/india/greycube-technologies) <sub> <img src="https://greycube.in/files/award.svg" width="25" height="25"> </sub>

<h5>
<sub><img src="https://greycube.in/files/link.svg" width="20" height="auto"> </sub> <a href="https://greycube.in"> greycube.in</a><br>
<sub><img src="https://greycube.in/files/8665305_envelope_email_icon.svg" width="20" height="18"> </sub> <a href="mailto:sales@greycube.in"> 
 sales@greycube.in</a><br>
<sub><img src="https://greycube.in/files/linkedin1.svg" width="20" height="18"> </sub> <a href="https://www.linkedin.com/company/greycube-technologies"> LinkedIn</a><br>
<sub><img src="https://greycube.in/files/blog.svg" width="20" height="18"> </sub><a href="https://greycube.in/blog"> Blogs</a> </h5>
