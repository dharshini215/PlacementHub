import re
import os 
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date
from models.application import Application
from models.company import Company
from database import db
from models.student import Student
from models.admin import Admin
from models.notification import Notification
from sqlalchemy import or_
from flask_mail import Mail, Message


app = Flask(__name__)

app.config.from_pyfile("config.py")

mail = Mail(app)

UPLOAD_FOLDER = "static/resumes"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf"}

db.init_app(app)

def send_email(to, subject, html):

    msg = Message(
        subject=subject,
        recipients=[to]
    )

    msg.html = html

    mail.send(msg)

def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_LOGO_FOLDER = "static/company_logos"

app.config["UPLOAD_LOGO_FOLDER"] = UPLOAD_LOGO_FOLDER


@app.route("/test-email")
def test_email():

    send_email(

        "YOUR_PERSONAL_EMAIL@gmail.com",

        "PlacementHub Test Email",

        """Hello,

This is a test email from PlacementHub.

Email configuration is working successfully.

Thank you.
"""
    )

    return "Email Sent Successfully!"

# -----------------------------------------
# Home
# -----------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------------
# Login
# -----------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        student = Student.query.filter_by(email=email).first()

        if student:

            if check_password_hash(student.password, password):

                session["student_id"] = student.id
                session["student_name"] = student.full_name

                flash("Login Successful!", "success")

                return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# -----------------------------------------
# Register
# -----------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        register_number = request.form.get("register_number")
        email = request.form.get("email")
        phone = request.form.get("phone")
        department = request.form.get("department")
        year = request.form.get("year")
        cgpa = request.form.get("cgpa")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Password Match
        if password != confirm_password:

            flash("Passwords do not match.", "danger")

            return render_template(
                "register.html",
                form=request.form
            )

        # Duplicate Email
        existing_email = Student.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return render_template(
        "register.html",
        form=request.form.to_dict()
    )

        # Duplicate Register Number
        existing_register = Student.query.filter_by(
            register_number=register_number
        ).first()

        if existing_register:

            flash("Register Number already exists.", "danger")

            return render_template(
        "register.html",
        form=request.form.to_dict()
            )

        # Hash Password
        hashed_password = generate_password_hash(password)

        # Create Student Object
        student = Student(

            full_name=full_name,
            register_number=register_number,
            email=email,
            phone=phone,
            department=department,
            year=year,
            cgpa=float(cgpa),
            password=hashed_password

        )

        db.session.add(student)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------------------
# Dashboard
# -----------------------------------------
@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:

        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    return render_template(
    "dashboard.html",
    student=student
)

# -----------------------------------------
# Edit Profile
# -----------------------------------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "student_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    if request.method == "POST":

        full_name = request.form.get("full_name").strip()
        phone = request.form.get("phone").strip()
        department = request.form.get("department")
        year = request.form.get("year")
        cgpa = request.form.get("cgpa")

        # ==========================
        # Full Name Validation
        # ==========================

        if not re.fullmatch(r"[A-Za-z ]{3,}", full_name):

            flash("Full Name should contain only letters and be at least 3 characters.", "danger")

            return render_template("edit_profile.html", student=student)

        # ==========================
        # Phone Validation
        # ==========================

        if not re.fullmatch(r"[6-9]\d{9}", phone):

            flash("Enter a valid Indian mobile number.", "danger")

            return render_template("edit_profile.html", student=student)

        # ==========================
        # CGPA Validation
        # ==========================

        try:

            cgpa = float(cgpa)

            if cgpa < 0 or cgpa > 10:

                flash("CGPA should be between 0 and 10.", "danger")

                return render_template("edit_profile.html", student=student)

        except ValueError:

            flash("Invalid CGPA.", "danger")

            return render_template("edit_profile.html", student=student)

        # ==========================
        # Save Data
        # ==========================

        student.full_name = full_name
        student.phone = phone
        student.department = department
        student.year = year
        student.cgpa = cgpa

        db.session.commit()

        flash("Profile Updated Successfully!", "success")

        return redirect(url_for("dashboard"))

        db.session.commit()

        flash("Profile Updated Successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template(
        "edit_profile.html",
        student=student
    )

# -----------------------------------------
# Resume
# -----------------------------------------

@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if "student_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    if request.method == "POST":

        if "resume" not in request.files:

            flash("No file selected.", "danger")

            return redirect(request.url)

        file = request.files["resume"]

        if not file.filename.lower().endswith(".pdf"):

            flash("Only PDF files are allowed.", "danger")

            return redirect(request.url)
        
            file.seek(0, 2)

            size = file.tell()

            file.seek(0)

            if size > 5 * 1024 * 1024:

                flash("Resume size should be less than 5 MB.", "danger")

                return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(
                student.register_number + ".pdf"
            )

            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            student.resume = filename

            db.session.commit()

            flash("Resume uploaded successfully!", "success")

            return redirect(url_for("dashboard"))

        flash("Only PDF files are allowed.", "danger")

    return render_template(
        "upload_resume.html",
        student=student
    )

# -----------------------------------------
# Drive
# -----------------------------------------

@app.route("/placement-drives")
def placement_drives():

    if "student_id" not in session:

        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    search = request.args.get("search", "").strip().lower()
    location = request.args.get("location", "").strip().lower()

    companies = Company.query.all()

    eligible_companies = []

    for company in companies:

        departments = [
            d.strip()
            for d in company.eligible_department.split(",")
        ]

        if (
            student.department in departments
            and student.cgpa >= company.minimum_cgpa
            and datetime.strptime(company.last_date, "%Y-%m-%d").date() >= date.today()
        ):

            if search:

                if (
                    search not in company.company_name.lower()
                    and search not in company.role.lower()
                ):
                    continue

            if location:

                if location not in company.location.lower():
                    continue

            eligible_companies.append(company)

    return render_template(
        "placement_drives.html",
        companies=eligible_companies
    )

# -----------------------------------------
# Apply Route
# -----------------------------------------

@app.route("/apply/<int:company_id>")
def apply_company(company_id):

    try:
        if "student_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        student_id = session["student_id"]

        existing = Application.query.filter_by(
            student_id=student_id,
            company_id=company_id
        ).first()

        if existing:
            flash("You have already applied for this company.", "warning")
            return redirect(url_for("placement_drives"))

        application = Application(
            student_id=student_id,
            company_id=company_id
        )

        db.session.add(application)
        db.session.commit()

        student = Student.query.get(student_id)
        company = Company.query.get(company_id)

        print("Student:", student)
        print("Company:", company)

        send_email(

            student.email,

            "🎉 Application Submitted Successfully",

            f"""
            <html>

            <body style="font-family:Arial;background:#f4f7fb;padding:30px;">

                <div style="max-width:650px;margin:auto;background:white;border-radius:10px;overflow:hidden;box-shadow:0 0 10px rgba(0,0,0,.1);">

                    <div style="background:#0d6efd;color:white;padding:20px;text-align:center;">

                        <h1>🎓 PlacementHub</h1>

                        <h3>Application Submitted Successfully</h3>

                    </div>

                    <div style="padding:30px;">

                        <p>Hello <b>{student.full_name}</b>,</p>

                        <p>
                        Your application has been successfully submitted.
                        </p>

                        <table style="width:100%;border-collapse:collapse;">

                            <tr>
                                <td><b>Company</b></td>
                                <td>{company.company_name}</td>
                            </tr>

                            <tr>
                                <td><b>Role</b></td>
                                <td>{company.role}</td>
                            </tr>

                            <tr>
                                <td><b>Package</b></td>
                                <td>{company.package}</td>
                            </tr>

                            <tr>
                                <td><b>Location</b></td>
                                <td>{company.location}</td>
                            </tr>

                            <tr>
                                <td><b>Status</b></td>
                                <td style="color:green;"><b>Applied</b></td>
                            </tr>

                        </table>

                        <br>

                        <p>
                        Please login to PlacementHub to track your application status.
                        </p>

                    </div>

                    <div style="background:#0d6efd;color:white;text-align:center;padding:15px;">

                        © 2026 PlacementHub<br>

                        Helping Students Build Their Careers

                    </div>

                </div>

            </body>

            </html>
            """

        )
        # Create Notification
        notification = Notification(
            student_id=student.id,
            message=f"You successfully applied for {company.company_name}."
)

        db.session.add(notification)
        db.session.commit()

        flash("Application Submitted Successfully!", "success")

        return redirect(url_for("placement_drives"))

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"<h2>Error:</h2><pre>{e}</pre>", 500

# -----------------------------------------2
# Applications
# -----------------------------------------

@app.route("/my-applications")
def my_applications():

    if "student_id" not in session:

        return redirect(url_for("login"))

    applications = Application.query.filter_by(
        student_id=session["student_id"]
    ).all()

    return render_template(
        "my_applications.html",
        applications=applications
    )


# -----------------------------------------
# Admin Login
# -----------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            session["admin_id"] = admin.id
            session["admin_username"] = admin.username

            flash("Admin Login Successful", "success")

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Username or Password", "danger")

    return render_template("admin_login.html")







# -----------------------------------------
# Admin Dashboard
# -----------------------------------------

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Company.query.count()      # One company = one drive
    resume_count = Student.query.filter(Student.resume.isnot(None)).count()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        resume_count=resume_count
    )

# -----------------------------------------
# Logout
# -----------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("login"))


# -----------------------------------------
# Admin - Students
# -----------------------------------------

@app.route("/admin/students")
def admin_students():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    year = request.args.get("year", "").strip()

    students = Student.query

    if search:
        students = students.filter(
            (Student.full_name.ilike(f"%{search}%")) |
            (Student.register_number.ilike(f"%{search}%"))
        )

    if department:
        students = students.filter(
            Student.department == department
        )

    if year:
        students = students.filter(
            Student.year == year
        )

    students = students.order_by(Student.full_name).all()

    return render_template(
        "admin_students.html",
        students=students
    )
# -----------------------------------------
# Admin - View Student
# -----------------------------------------

@app.route("/admin/student/<int:id>")
def view_student(id):

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))

    student = Student.query.get_or_404(id)

    return render_template(

        "view_student.html",

        student=student

    )

# -----------------------------------------
#  admin appilation
# -----------------------------------------

@app.route("/admin/applications")
def admin_applications():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    applications = Application.query.order_by(
        Application.applied_on.desc()
    ).all()

    return render_template(
        "admin_applications.html",
        applications=applications
    )


# -----------------------------------------
#  Status Update Route
# -----------------------------------------

@app.route("/admin/application/<int:id>", methods=["GET","POST"])
def update_application(id):

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))

    application = Application.query.get_or_404(id)

    if request.method == "POST":

        application.status = request.form.get("status")
        status = application.status

        student = Student.query.get(application.student_id)

        company = Company.query.get(application.company_id)

        db.session.commit()

        send_email(

    student.email,

    f"Application Status Updated - {company.company_name}",

    f"""
    <html>

    <body style="font-family:Arial;background:#f4f7fb;padding:30px;">

    <div style="max-width:650px;
                margin:auto;
                background:white;
                border-radius:10px;
                overflow:hidden;
                box-shadow:0 0 10px rgba(0,0,0,.15);">

        <div style="background:#0d6efd;
                    color:white;
                    padding:20px;
                    text-align:center;">

            <h2>PlacementHub</h2>

            <h3>Application Status Updated</h3>

        </div>

        <div style="padding:30px;">

            <p>Hello <b>{student.full_name}</b>,</p>

            <p>Your application status has been updated.</p>

            <table style="width:100%;border-collapse:collapse;">

                <tr>
                    <td><b>Company</b></td>
                    <td>{company.company_name}</td>
                </tr>

                <tr>
                    <td><b>Role</b></td>
                    <td>{company.role}</td>
                </tr>

                <tr>
                    <td><b>Current Status</b></td>
                    <td><b>{status}</b></td>
                </tr>

            </table>

            <br>

            <p>
            Please login to PlacementHub for more details.
            </p>

        </div>

        <div style="background:#0d6efd;
                    color:white;
                    text-align:center;
                    padding:15px;">

            © 2026 PlacementHub

        </div>

    </div>

    </body>

    </html>

    """
)

        student = application.student
        company = application.company

        send_email(

            student.email,

            "Application Status Updated",

            f"""
        Hello {student.full_name},

        Your application status has been updated.

        Company : {company.company_name}

        Role : {company.role}

        Current Status : {application.status}

        Please login to PlacementHub for more details.

        Regards,
        PlacementHub Team
        """
        )

        flash("Application Updated Successfully", "success")

        return redirect(url_for("admin_applications"))

    return render_template(
        "update_application.html",
        application=application
    )



# -----------------------------------------
#  Company
# -----------------------------------------

@app.route("/admin/companies")
def admin_companies():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    status = request.args.get("status", "").strip()

    companies = Company.query

    if status == "open":
        companies = companies.filter(Company.is_active == True)

    elif status == "closed":
        companies = companies.filter(Company.is_active == False)

    companies = companies.order_by(
        Company.company_name
    ).all()
    status = request.args.get("status", "").strip()

    print("Selected Status:", status)

    companies = Company.query

    if status == "open":
        print("Filtering OPEN")
        companies = companies.filter(Company.is_active == True)

    elif status == "closed":
        print("Filtering CLOSED")
        companies = companies.filter(Company.is_active == False)

    companies = companies.order_by(Company.company_name).all()

    print("Companies Returned:")
    for c in companies:
        print(c.company_name, c.is_active)


    return render_template(
        "admin_companies.html",
        companies=companies
    )

# -----------------------------------------
# Add Company
# -----------------------------------------

@app.route("/admin/add-company", methods=["GET", "POST"])
def add_company():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        logo = request.files.get("logo")

        logo_filename = None

        if logo and logo.filename != "":

            logo_filename = secure_filename(logo.filename)

            logo.save(
                os.path.join(
                    app.config["UPLOAD_LOGO_FOLDER"],
                    logo_filename
                )
            )

        company = Company(

            company_name=request.form.get("company_name"),

            role=request.form.get("role"),

            package=request.form.get("package"),

            location=request.form.get("location"),

            eligible_department=",".join(
                request.form.getlist("eligible_department")
            ),

            minimum_cgpa=float(request.form.get("minimum_cgpa")),

            last_date=request.form.get("last_date"),

            logo=logo_filename

        )

        db.session.add(company)
        db.session.commit()

        # -----------------------------
        # Notify Eligible Students
        # -----------------------------

        departments = [
            d.strip()
            for d in company.eligible_department.split(",")
        ]

        students = Student.query.all()

        for student in students:

            if (
                student.department in departments
                and student.cgpa >= company.minimum_cgpa
            ):

                # Save Notification
                notification = Notification(

                    student_id=student.id,

                    message=f"New placement drive available: {company.company_name} ({company.role})"

                )

                db.session.add(notification)

                # Send Email
                send_email(

                    student.email,

                    f"New Placement Drive - {company.company_name}",

                    f"""
        Hello {student.full_name},

        A new placement opportunity matching your profile has been posted.

        Company : {company.company_name}

        Role : {company.role}

        Package : {company.package}

        Location : {company.location}

        Minimum CGPA : {company.minimum_cgpa}

        Last Date : {company.last_date}

        Please login to PlacementHub and apply before the deadline.

        Regards,

        PlacementHub Team
        """

                )

        departments = [d.strip() for d in company.eligible_department.split(",")]

        print("Eligible Departments:", departments)

        students = Student.query.all()

        for student in students:

            print("----------------------")
            print("Student:", student.full_name)
            print("Department:", student.department)
            print("CGPA:", student.cgpa)

            if (
                student.department in departments
                and student.cgpa >= company.minimum_cgpa
            ):

                print("MATCH FOUND:", student.full_name)

                notification = Notification(
                    student_id=student.id,
                    message=f"New placement drive available: {company.company_name} ({company.role})"
                )

                db.session.add(notification)

        db.session.commit()

        flash("Company Added Successfully!", "success")

        return redirect(url_for("admin_companies"))

    return render_template("add_company.html")


# -----------------------------------------
# Edit Company
# -----------------------------------------

@app.route("/admin/edit-company/<int:id>", methods=["GET", "POST"])
def edit_company(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    company = Company.query.get_or_404(id)

    if request.method == "POST":

        company.company_name = request.form.get("company_name")
        company.role = request.form.get("role")
        company.package = request.form.get("package")
        company.location = request.form.get("location")
        company.eligible_department = ",".join(
    request.form.getlist("eligible_department")
)
        company.minimum_cgpa = float(request.form.get("minimum_cgpa"))
        company.last_date = request.form.get("last_date")

        db.session.commit()

        flash("Company Updated Successfully!", "success")

        return redirect(url_for("admin_companies"))

    return render_template(
        "edit_company.html",
        company=company
    )


# -----------------------------------------
# Delete Company
# -----------------------------------------

@app.route("/admin/company/delete/<int:id>")
def delete_company(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    company = Company.query.get_or_404(id)

    db.session.delete(company)
    db.session.commit()

    flash("Company deleted successfully!", "success")

    return redirect(url_for("admin_companies"))


# -----------------------------------------
# Company Status
# -----------------------------------------

@app.route("/admin/company/status/<int:id>")
def change_company_status(id):

    company = Company.query.get_or_404(id)

    company.is_active = not company.is_active

    db.session.commit()

    flash("Company status updated successfully.", "success")

    return redirect(url_for("admin_companies"))



# -----------------------------------------
# notification
# -----------------------------------------

@app.route("/notifications")
def notifications():

    if "student_id" not in session:

        return redirect(url_for("login"))

    notifications = Notification.query.filter_by(

        student_id=session["student_id"]

    ).order_by(

        Notification.created_at.desc()

    ).all()

    return render_template(

        "notifications.html",

        notifications=notifications

    )



# -----------------------------------------
# Company Details
# -----------------------------------------

@app.route("/company/<int:company_id>")
def company_details(company_id):

    if "student_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("login"))

    company = Company.query.get_or_404(company_id)

    return render_template(
        "company_details.html",
        company=company
    )


# -----------------------------------------
# Main
# -----------------------------------------
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True,
    use_reloader=False
)
