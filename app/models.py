from dbconnector import connect_database, disconnect_database
from mysql.connector import Error
import settings as sett
import hashlib
from datetime import datetime

# Utility Functions
def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# User Management Functions
def login_user(email, password):
    """Logs in a user by checking their email and hashed password in the database."""
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        sett.mycursor.execute(query, (email, hashed_password))
        user = sett.mycursor.fetchone()
        if user:
            return user
        else:
            return None
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def register_user(name, studentID, mobile_no, email, dob, address, password):
    """Registers a new user in the database."""
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "INSERT INTO user (name, studentID, mobile_no, email, dob, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (name, studentID, mobile_no, email, dob, address, hashed_password))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_user_profile(studentID):
    """Fetches user profile and their job applications from the database."""
    connect_database()
    try:
        query = "SELECT * FROM user WHERE studentID = %s"
        sett.mycursor.execute(query, (studentID,))
        user = sett.mycursor.fetchone()

        query = "SELECT a.appid, j.title, a.appdate, a.status FROM application a JOIN job j ON a.jobID = j.jobID WHERE a.studentID = %s"
        sett.mycursor.execute(query, (studentID,))
        applications = sett.mycursor.fetchall()

        return user, applications
    except Error as e:
        print(f"Error: '{e}'")
        return None, None
    finally:
        disconnect_database()

def update_user_profile(studentID, name, mobile_no, email, dob, address, password):
    """Updates user profile information in the database."""
    connect_database()
    try:
        hashed_password = hash_password(password) if password else None
        query = "UPDATE user SET name = %s, mobile_no = %s, email = %s, dob = %s, address = %s"
        params = [name, mobile_no, email, dob, address]
        if hashed_password:
            query += ", password = %s"
            params.append(hashed_password)
        query += " WHERE studentID = %s"
        params.append(studentID)

        sett.mycursor.execute(query, tuple(params))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

# Company Management Functions
def login_company(companyID, password):
    """Logs in a company by checking their ID and hashed password in the database."""
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "SELECT * FROM company WHERE companyID = %s AND password = %s"
        sett.mycursor.execute(query, (companyID, hashed_password))
        company = sett.mycursor.fetchone()
        if company:
            return company
        else:
            return None
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def register_company(companyID, name, industries, address, contact_person, contact_address, password):
    """Registers a new company in the database."""
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "INSERT INTO company (companyID, name, industries, address, contact_person, contact_address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (companyID, name, industries, address, contact_person, contact_address, hashed_password))
        sett.connection.commit()
        return companyID
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def get_company_details(companyID):
    """Fetches company details and their job postings from the database."""
    connect_database()
    try:
        query = "SELECT * FROM company WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        company = sett.mycursor.fetchone()

        query = "SELECT * FROM job WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        jobs = sett.mycursor.fetchall()

        return company, jobs
    except Error as e:
        print(f"Error: '{e}'")
        return None, None
    finally:
        disconnect_database()

def get_companies():
    """Fetches all companies from the database."""
    connect_database()
    try:
        query = "SELECT * FROM company"
        sett.mycursor.execute(query)
        companies = sett.mycursor.fetchall()
        return companies
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def get_company_jobs(companyID):
    """Fetches all job postings of a specific company from the database."""
    connect_database()
    try:
        query = "SELECT * FROM job WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        jobs = sett.mycursor.fetchall()
        return jobs
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        disconnect_database()

def create_job(jobID, companyID, title, description, required_skills, salary, location):
    """Creates a new job posting for a company in the database."""
    connect_database()
    try:
        query = "INSERT INTO job (jobID, companyID, title, description, required_skills, salary, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (jobID, companyID, title, description, required_skills, salary, location))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_company_applications(companyID):
    """Fetches all job applications for jobs posted by a specific company from the database."""
    connect_database()
    try:
        query = """
        SELECT a.appid, a.studentID, j.title, a.appdate, a.status, u.name, u.email, u.mobile_no, u.dob
        FROM application a
        JOIN job j ON a.jobID = j.jobID
        JOIN user u ON a.studentID = u.studentID
        WHERE j.companyID = %s
        ORDER BY a.jobID
        """
        sett.mycursor.execute(query, (companyID,))
        applications = sett.mycursor.fetchall()
        return applications
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        disconnect_database()

# Job Application Functions
def apply_for_job(appID, studentID, jobID, file_path):
    """Applies for a job by inserting a new application record into the database."""
    connect_database()
    try:
        appdate = datetime.now().strftime('%Y-%m-%d')
        query = """
            INSERT INTO application (appid, studentID, jobID, appdate, status, file_path)
            VALUES (%s, %s, %s, %s, 'applied', %s)
        """
        sett.mycursor.execute(query, (appID, studentID, jobID, appdate, file_path))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_resume_path(appid):
    """Fetches the file path of the resume for a specific application from the database."""
    connect_database()
    try:
        query = "SELECT file_path FROM application WHERE appid = %s"
        sett.mycursor.execute(query, (appid,))
        result = sett.mycursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def update_application_status_db(appid, status):
    """Updates the status of a specific job application in the database."""
    connect_database()
    try:
        query = "UPDATE application SET status = %s WHERE appid = %s"
        sett.mycursor.execute(query, (status, appid))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()
