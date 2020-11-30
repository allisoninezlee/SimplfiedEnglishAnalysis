from datetime import *
from getpass import getpass
import mysql.connector

#Gather system information for connecting to MySQL
print("Please provide the following information about the MySQL server where data should be stored...")
session_host = input("The host name or IP address of the MySQL server (e.g. localhost): ")
session_user = input("The user name used to authenticate with the MySQL server (e.g. root): ")
session_password = getpass("The password to authenticate the user with the MySQL server: ")
#Note: getpass() will give a warning if code is run on IDLE instead of a terminal

#Create connection to MySQL
connection = mysql.connector.connect(
  host = session_host,
  user = session_user,
  password = session_password
)

#Get datetime and format for database name
current_dt = datetime.now()
db_name = "vocab" + "_" + str(current_dt.year) + "-" + str(current_dt.month) + "-" + str(current_dt.day) + "_" + str(current_dt.hour).zfill(2) + str(current_dt.minute).zfill(2) + str(current_dt.second).zfill(2)
print(db_name)

#Create new database
cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS `%s`" % (db_name)) #include backticks to allow hyphens in name
cursor.execute("CREATE DATABASE `%s`" % (db_name))

#Reestablish connection with newly created database
connection = mysql.connector.connect(
  host = session_host,
  user = session_user,
  password = session_password,
  database = db_name
)

#Create tables within database
cursor = connection.cursor()
cursor.execute("CREATE TABLE noun (noun_id INT AUTO_INCREMENT PRIMARY KEY, noun_text VARCHAR(250), num_occur INT)")
cursor.execute("CREATE TABLE sentence (sentence_id INT AUTO_INCREMENT PRIMARY KEY, sentence_text VARCHAR(1000), document_id INT)")
cursor.execute("CREATE TABLE document (document_id INT AUTO_INCREMENT PRIMARY KEY, document_name VARCHAR(250), publication_year INT, product VARCHAR(250), location VARCHAR(1000))")
cursor.execute("CREATE TABLE noun_in_sentence (noun_sentence_id INT AUTO_INCREMENT PRIMARY KEY, noun_id INT, FOREIGN KEY(noun_id) REFERENCES noun(noun_id), sentence_id INT, FOREIGN KEY(sentence_id) REFERENCES sentence(sentence_id), document_id INT, FOREIGN KEY(document_id) REFERENCES document(document_id))")


