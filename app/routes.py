from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory   
from app.models import *
from app.utils import *
from werkzeug.utils import secure_filename
import os
from flask import current_app as app

main = Blueprint('main', __name__)

# Home Route
@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# User Login Route
@main.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = login_user(email, password)
        if user:
            session['user'] = user
            return redirect(url_for('main.user_profile'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('main.user_login'))
    return render_template('user_login.html')

# Company Login Route
@main.route('/company_login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        companyID = request.form['companyID']
        password = request.form['password']
        company = login_company(companyID, password)
        if company:
            session['company'] = company
            return redirect(url_for('main.company_profile'))
        else:
            flash("Invalid Company ID or password")
            return redirect(url_for('main.company_login'))
    return render_template('company_login.html')

# User Registration Route
@main.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('main.user_register'))

        studentID = generate_unique_studentID()

        if register_user(name, studentID, mobile_no, email, dob, address, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('main.user_login'))
        else:
            flash("Registration failed. Please try again.")

    return render_template('user_register.html')

# Company Registration Route
@main.route('/company_register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        name = request.form['name']
        industries = request.form['industries']
        address = request.form['address']
        contact_person = request.form['contact_person']
        contact_address = request.form['contact_address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('main.company_register'))

        companyID = generate_unique_companyID()

        if register_company(companyID, name, industries, address, contact_person, contact_address, password):
            flash("Registration successful! Please log in.")
            return render_template('company_success.html', companyID=companyID)
        else:
            flash("Registration failed. Please try again.")
            return redirect(url_for('main.company_register'))

    return render_template('company_register.html')

# User Profile Route
@main.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if 'user' not in session:
        return redirect(url_for('main.home'))

    studentID = session['user'][1]

    if request.method == 'POST':
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        dob = request.form['dob']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password and password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('main.user_profile'))

        if update_user_profile(studentID, name, mobile_no, email, dob, address, password):
            flash("Profile updated successfully")
        else:
            flash("Failed to update profile")

    user, applications = get_user_profile(studentID)
    return render_template('user_profile.html', user=user, applications=applications)

# Company Profile Route
@main.route('/company_profile', methods=['GET'])
def company_profile():
    if 'company' not in session:
        return redirect(url_for('main.company_login'))

    company = session['company']
    companyID = company[0]
    applications = get_company_applications(companyID)

    return render_template('company_profile.html', company=company, applications=applications)

# User Companies Route
@main.route('/user_companies')
def user_companies():
    companies = get_companies()
    return render_template('user_companies.html', companies=companies)

# User Company Route
@main.route('/user_company/<int:companyID>')
def user_company(companyID):
    company, jobs = get_company_details(companyID)
    return render_template('user_company.html', company=company, jobs=jobs)

# Apply for Job Route
@main.route('/apply/<int:jobID>', methods=['GET', 'POST'])
def apply(jobID):
    appID = generate_unique_appID()
    
    # Ensure user is in session and is a tuple
    if 'user' not in session:
        return redirect(url_for('main.home'))

    # Access the studentID from the tuple
    studentID = session['user'][1]

    if request.method == 'POST':
        if 'resume' not in request.files:
            flash("No file part", 'danger')
            return redirect(request.url)
        file = request.files['resume']
        
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)

            if apply_for_job(appID, studentID, jobID, file_path):
                flash("Applied for job successfully", 'success')
                # return redirect(url_for('main.user_profile'))
            else:
                flash("Application can be applied only once", 'danger')
                return render_template('application.html', jobID=jobID)
        else:
            flash("Invalid file type or file too large", 'danger')
            return render_template('application.html', jobID=jobID)

    return render_template('application.html', jobID=jobID)

# Download Resume Route
@main.route('/download_resume/<int:appid>', methods=['GET'])
def download_resume(appid):
    if 'company' not in session:
        return redirect(url_for('main.company_login'))

    # Get the file path from the database using the application ID
    file_path = get_resume_path(appid)

    if file_path:
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        flash("File not found", "danger")
        return redirect(url_for('main.company_profile'))

# Company Jobs Route
@main.route('/company_jobs')
def company_jobs():
    if 'company' not in session:
        return redirect(url_for('main.company_login'))

    companyID = session['company'][0]
    company = session['company']
    jobs = get_company_jobs(companyID)  # A function to retrieve jobs for the company

    return render_template('company_jobs.html', company=company, jobs=jobs)

# Add Job Route
@main.route('/add_job', methods=['POST'])
def add_job():
    jobID = generate_unique_jobID()
    if 'company' not in session:
        return redirect(url_for('main.company_login'))

    companyID = session['company'][0]
    title = request.form['title']
    description = request.form['description']
    required_skills = request.form['required_skills']
    salary = request.form['salary']
    location = request.form['location']

    if create_job(jobID, companyID, title, description, required_skills, salary, location):  # A function to insert a job into the database
        flash("Job added successfully")
    else:
        flash("Failed to add job")

    return redirect(url_for('main.company_jobs'))

# Update Application Status Route
@main.route('/update_application_status/<int:appid>', methods=['POST'])
def update_application_status(appid):
    if 'company' not in session:
        return redirect(url_for('main.company_login'))

    status = request.form['status']
    if update_application_status_db(appid, status):
        flash("Application status updated successfully", "success")
    else:
        flash("Failed to update application status", "danger")

    return redirect(url_for('main.company_profile'))

# Logout Route
@main.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('company', None)
    return redirect(url_for('main.home'))
