import argparse
import os
from os import path
from document import Document
import parsers
import database
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True, help='path to file to parse')
    parser.add_argument('--database', '-d', type=bool, default=False, required=False, help='triggers the use of a mysql database')
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
    #       (airplane vs Airplane) and the same with singular/plural nouns (airplane vs airplanes)
    total_nouns = parsers.get_nouns(total_sentences)

    if args.database is True:
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
        database.insert_noun_in_sent(total_nouns, connection)

        connection.close()
        print("Data has been successfully exported to the database %s", db_name)
    else:
        # Open csv files to write to
        csv_name = doc1.document_name + '_nouns.csv'
        with open(csv_name, 'w', newline='') as csvfile:
            nounwriter = csv.writer(csvfile)
            nounwriter.writerow([doc1.document_name, doc1.pub_year, doc1.product,doc1.location])
            for noun in total_nouns:
                nounwriter.writerow([noun.text, noun.context_sentences, noun.num_occur])
            print('Data has been successfully saved to ' + csv_name)

