from dbconnector import connect_database, disconnect_database
from mysql.connector import Error
import settings as sett
import random

def generate_unique_studentID():
    while True:
        studentID = str(random.randint(100000, 999999))
        if not uid_exists(studentID):
            return studentID
        
def uid_exists(uid):
    connect_database()
    try:
        query = "SELECT studentID FROM user WHERE studentID = %s"
        sett.mycursor.execute(query, (uid,))
        result = sett.mycursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def generate_unique_companyID():
    while True:
        companyID = str(random.randint(100000, 999999))
        connect_database()
        try:
            query = "SELECT companyID FROM company WHERE companyID = %s"
            sett.mycursor.execute(query, (companyID,))
            result = sett.mycursor.fetchone()
            if result is None:
                return companyID
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            disconnect_database()

def generate_unique_appID():
    while True:
        appID = str(random.randint(100000, 999999))
        connect_database()
        try:
            query = "SELECT appid FROM application WHERE appid = %s"
            sett.mycursor.execute(query, (appID,))
            result = sett.mycursor.fetchone()
            if result is None:
                return appID
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            disconnect_database()
def generate_unique_jobID():
    while True:
        jobID = str(random.randint(100000, 999999))
        connect_database()
        try:
            query = "SELECT jobID FROM application WHERE jobID = %s"
            sett.mycursor.execute(query, (jobID,))
            result = sett.mycursor.fetchone()
            if result is None:
                return jobID
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            disconnect_database()