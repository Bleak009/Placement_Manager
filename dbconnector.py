import mysql.connector
from mysql.connector import Error
import settings as sett

def connect_database():
    try:
        sett.connection = mysql.connector.connect(
            host=sett.DB_HOST,
            database=sett.DB_NAME,
            user=sett.DB_USER,
            password=sett.DB_PASSWORD
        )
        sett.mycursor = sett.connection.cursor()
        print("Connected to MySQL Server")
    except Error as e:
        print("Error while connecting to MySQL", e)

def disconnect_database():
    if sett.mycursor and sett.connection:
        sett.mycursor.close()
        sett.connection.close()
        print("MySQL connection is closed")

def create_database():
    user = '''CREATE TABLE IF NOT EXISTS user (
    name VARCHAR(255) NOT NULL,
    studentID BIGINT PRIMARY KEY,
    mobile_no VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    dob DATE NOT NULL,
    address TEXT NOT NULL,
    password VARCHAR(255) NOT NULL);'''

    company = '''CREATE TABLE IF NOT EXISTS company (
    companyID BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industries TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_person VARCHAR(255) NOT NULL,
    contact_address TEXT NOT NULL,
    password VARCHAR(255) NOT NULL);'''

    job = '''CREATE TABLE IF NOT EXISTS job (
    jobID BIGINT PRIMARY KEY,
    companyID BIGINT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills VARCHAR(255) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    FOREIGN KEY (companyID) REFERENCES company(companyID));'''

    application = '''CREATE TABLE IF NOT EXISTS application (
    appid BIGINT UNIQUE,
    studentID BIGINT NOT NULL,
    jobID BIGINT NOT NULL,
    appdate DATE NOT NULL,
    status ENUM('applied', 'interview', 'offered', 'rejected') NOT NULL,
    file_path VARCHAR(255),
    PRIMARY KEY (studentID, jobID),
    FOREIGN KEY (studentID) REFERENCES user(studentID),
    FOREIGN KEY (jobID) REFERENCES job(jobID));'''    

    connect_database()
    sett.mycursor.execute(user)
    sett.mycursor.execute(company)
    sett.mycursor.execute(job)
    sett.mycursor.execute(application)
    disconnect_database()
