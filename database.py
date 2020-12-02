from datetime import *
from getpass import getpass # Note: getpass() will give a warning if code is run on IDLE instead of a terminal
import mysql.connector
from mysql.connector import Error

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: get_server_info

description: Prompts user for information about the server
they want the database created on

parameters: No parameters

returns: Server's host, username, and password
'''''''''''''''''''''''''''''''''''''''''''''''''''
def get_server_info():
  # Gather system information for connecting to MySQL server
  print("Please provide the following information about the MySQL server where data should be stored...")
  session_host = input("The host name or IP address of the MySQL server (e.g. localhost): ")
  session_user = input("The user name used to authenticate with the MySQL server (e.g. root): ")
  session_password = getpass("The password to authenticate the user with the MySQL server: ")

  return (session_host, session_user, session_password)

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: create_database

description: Uses server information provided by user
to create a new MySQL database for the program session

parameters: Server's host, username, and password

returns: Name of new database
'''''''''''''''''''''''''''''''''''''''''''''''''''
def create_database(session_host, session_user, session_password):

  #Create connection to MySQL server
  connection = mysql.connector.connect(
    host = session_host,
    user = session_user,
    password = session_password
  )

  #Get datetime and format for database name
  current_dt = datetime.now()
  db_name = "vocab" + "_" + str(current_dt.year) + "-" + str(current_dt.month) + "-" + str(current_dt.day) + "_" + str(current_dt.hour).zfill(2) + str(current_dt.minute).zfill(2) + str(current_dt.second).zfill(2)

  #Create new database
  cursor = connection.cursor()
  cursor.execute("DROP DATABASE IF EXISTS `%s`" % (db_name))
  cursor.execute("CREATE DATABASE `%s`" % (db_name))

  cursor.close()
  return db_name

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: connect_database

description: Creates connection to new database within the server

parameters: Name of database, server's host, username, and password

returns: The database connection object
'''''''''''''''''''''''''''''''''''''''''''''''''''
def connect_database(session_host, session_user, session_password, db_name):
  # Establish connection with newly created database in the server
  connection = mysql.connector.connect(
    host = session_host,
    user = session_user,
    password = session_password,
    database = db_name
  )
  return connection

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: create_tables

description: Creates four empty tables within the database

parameters: The database connection object 

returns: None
'''''''''''''''''''''''''''''''''''''''''''''''''''
def create_tables(connection):

  #Create tables within database
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE noun (noun_id INT AUTO_INCREMENT PRIMARY KEY, noun_text VARCHAR(250), num_occur INT)")
  cursor.execute("CREATE TABLE sentence (sentence_id INT AUTO_INCREMENT PRIMARY KEY, sentence_text VARCHAR(1000), document_id INT)")
  cursor.execute("CREATE TABLE document (document_id INT AUTO_INCREMENT PRIMARY KEY, document_name VARCHAR(250), publication_year INT, product VARCHAR(250), location VARCHAR(1000))")
  cursor.execute("CREATE TABLE noun_in_sentence (noun_sentence_id INT AUTO_INCREMENT PRIMARY KEY, noun_id INT, FOREIGN KEY(noun_id) REFERENCES noun(noun_id), sentence_id INT, FOREIGN KEY(sentence_id) REFERENCES sentence(sentence_id), document_id INT, FOREIGN KEY(document_id) REFERENCES document(document_id))")

  cursor.close()
  return

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: insert_documents

description: Inserts information from the document object into the document table

parameters: The document object and the database connection object 

returns: None
'''''''''''''''''''''''''''''''''''''''''''''''''''
def insert_documents(document, connection):

  cursor = connection.cursor()
  query = "INSERT INTO document (document_name, publication_year, product, location) VALUES (%s, %s, %s, %s)"
  args = (document.document_name, document.pub_year, document.product, document.location)

  try:
    cursor.execute(query, args)
    connection.commit()

  except Error as error:
    print(error)

  cursor.close()
  return

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: insert_sentences

description: Inserts information from list of span/sentence objects into the sentence table

parameters: The list of span/sentence objects and the database connection object 

returns: None
'''''''''''''''''''''''''''''''''''''''''''''''''''
def insert_sentences(total_sentences, connection):
  cursor = connection.cursor()
  query = "INSERT INTO sentence (sentence_text, document_id) VALUES (%s, %s)"

  for sentence in total_sentences:
    try:
      args = (sentence.text, 1)   # Hard code for now until we accept multiple documents
      cursor.execute(query, args)
      connection.commit()

    except Error as error:
      print(error)

  cursor.close()
  return

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: insert_nouns

description: Inserts information from list of noun objects into the noun table

parameters: The list of noun objects and the database connection object 

returns: None
'''''''''''''''''''''''''''''''''''''''''''''''''''
def insert_nouns(total_nouns, connection):
  cursor = connection.cursor()
  query = "INSERT INTO noun (noun_text, num_occur) VALUES (%s, %s)"

  for noun in total_nouns:
    args = (noun.text, noun.num_occur)

    try:
      cursor.execute(query, args)
      connection.commit()

    except Error as error:
      print(error)

  cursor.close()
  return

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: insert_noun_in_sent

description: Inserts foreign keys into noun_in_sentence table to complete
the relational database

parameters: list of noun objects, connection to database

returns: None

*Note: This can be combined later with insert_nouns() to remove a for-loop 
       and improve running time. Will leave it like this for now so we can
       easily understand how each table is filled
'''''''''''''''''''''''''''''''''''''''''''''''''''
def insert_noun_in_sent(total_nouns, connection):
  # for each noun in the noun objects:
  #     get the its noun_id from the noun table
  #     for each context sentence of that noun:
  #         get its sentence_id from the sentence table
  #         get the document's doc_id from the sentence table
  #         insert entry into noun_in_sentence table

  cursor = connection.cursor()

  for noun in total_nouns:
    try:
      cursor.execute("SELECT noun_id FROM noun WHERE noun_text = %s", (noun.text,))
      noun_id = cursor.fetchall()[0][0]   # MySQL will return this as [(noun_id,)], so grab just the element

      for sentence in noun.context_sentences:
        cursor.execute("SELECT sentence_id, document_id FROM sentence WHERE sentence_text = %s", (sentence.text,))
        (sentence_id, document_id) = cursor.fetchall()[0]

        cursor.execute("INSERT INTO noun_in_sentence (noun_id, sentence_id, document_id) VALUES (%s, %s, %s)", (noun_id, sentence_id, document_id))
        connection.commit()

    except Error as error:
      print(error)

  cursor.close()
  return
