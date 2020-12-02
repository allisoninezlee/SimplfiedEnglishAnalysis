import argparse
import os
from os import path
from noun import Noun
from document import Document
import parsers
import database

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True, help='path to file to parse and add to database.')
    args = parser.parse_args()
    
    file_path = args.file

    # check for valid path
    if not path.exists(file_path):
        print("File " + file_path + " does not exist. Exiting...")
        exit()
    
    print("Processing file: " + args.file)

    # open file
    pdf = parsers.open_pdf(file_path)
    text = parsers.extract_text(pdf)

    # create document object for this pdf
    # (hard coding some attributes until we have an algorithm to get this info directly from reading PDF)
    doc1 = Document(pdf, 'Document 1', 2020, 'Airplane', file_path)

    # get list of span objects - one for each sentence in pdf file
    total_sentences = parsers.get_sentences(text)

    # get list of token (noun) objects
    # note: we'll need to adjust so that the same noun with different capitalization isn't picked up twice
    #       (airplane vs Airplane)
    total_nouns = parsers.get_nouns(total_sentences)

    for noun in total_nouns:
        print(noun.text, noun.num_occur)

    # Get server information from user and create a new database in the server
    (session_host, session_user, session_password) = database.get_server_info()
    db_name = database.create_database(session_host, session_user, session_password)

    # Create connection to this new database & store database connection object for further use
    connection = database.connect_database(session_host, session_user, session_password, db_name)

    # Create tables in database
    database.create_tables(connection)

    # Insert information into tables
    database.insert_documents(doc1, connection)
    database.insert_sentences(total_sentences, connection)
    database.insert_nouns(total_nouns, connection)
    #database.insert_noun_in_sent()   # work in progress

    connection.close()

    print("Data has been successfully exported to the database %s", db_name)

