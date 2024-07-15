# Placement_Manager
 DBMS project 2024

# Pre-requisites:
	1. Python 3.11 or higher
    2. Python Modules - Flask, MySQL-connector-python, werkzeug
	3. MySQL sever and command line
 	4. Windows OS

# Steps to setup and run the placement management system locally:

 1. Download all the files and extract them into a directory.
 2. Use the following commands to install the required modules
    >pip install flask <br>pip install mysql-connector-python
4. Install MySQL server and create database using sql query (refer aql_queries.txt) in the command line client.
   >https://dev.mysql.com/downloads/installer/ <--Download the installer from this link and install the server and command line client.<br>
   >--Select <b>full install</b> for installation type. <br> 
   >--Run MySql command line client after installation.<br>
   >--Refer sql_queries.txt for creating database.<br>
   >--Alternatively you can use MySQL workbench to create the database.
5. Modify dbconnector.py with your database details (password and database_name).
6. Open command propmt/Powershell in the downloaded directory and type "run.py" to start the server.
7. The placement management system is now live.
