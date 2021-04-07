import argparse
import os
from os import path
from document import Document
import parsers
import database
import csv
from PyPDF2 import PdfFileReader
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True, nargs='+', help='path to file to parse')
    parser.add_argument('--database', '-d', action='store_true', required=False, help='triggers the use of a mysql database')
    args = parser.parse_args()
    
    for file_path in args.file:
        # check for valid path
        if not path.exists(file_path):
            print("File " + file_path + " does not exist. Exiting...")
            exit()
    
        print("Processing file: " + file_path)

        # start timer
        startTime = time.time()

        # open file
        pdf = parsers.open_pdf(file_path)
        text = parsers.extract_text(pdf)

        # get document info
        with open(file_path, 'rb') as f:
            reader = PdfFileReader(f)
            reader.getNumPages() # work around for decrpyting file
            docInfo = reader.getDocumentInfo()
        
        # make list of all attributes
        docAttributes = []
        for attribute in docInfo:
            docAttributes.append(attribute[1:] + ": " + docInfo[attribute])        

        # Perform parsing and identification
        total_sentences = parsers.get_sentences(text)  # get list of span objects - one for each sentence in pdf file
        total_nouns = parsers.get_nouns(total_sentences)   # get list of token (noun) objects
        parsers.get_noun_phrases(total_sentences, total_nouns)   # find noun phrases

        # end timer
        elapsedTime = time.time() - startTime
        totalTimeStr = "Total time: " + str(round(elapsedTime, 3)) + " sec" # used in .csv file

        # calculate unique nouns, total nouns
        unqNouns = len(total_nouns)
        sumNouns = 0       
        for noun in total_nouns:
            sumNouns += noun.num_occur

        # calculate cost per noun in milliseconds
        costPerNoun = (elapsedTime * 1000) / sumNouns
        costPerNounStr = "Cost per noun: " + str(round(costPerNoun, 3)) + " ms" # used in .csv file
    

        if args.database is True:
            # Get server information from user and create a new database in the server
            (session_host, session_user, session_password) = database.get_server_info()
            db_name = database.create_database(session_host, session_user, session_password)

            # Create connection to this new database & store database connection object for further use
            connection = database.connect_database(session_host, session_user, session_password, db_name)

            # Create tables in database
            database.create_tables(connection)

            # Insert information into tables
            database.insert_documents(docAttributes, connection)
            database.insert_sentences(total_sentences, connection)
            database.insert_nouns(total_nouns, connection)
            database.insert_noun_in_sent(total_nouns, connection)

            connection.close()
            print("Data has been successfully exported to the database %s", db_name)
        else:
            # Open csv files to write to
            if docInfo.title != None:
                csv_name = docInfo.title + '_nouns.csv'
            else:
                csv_name = (file_path.split('/'))[-1][:-4] + '_nouns.csv' # get name of file from file_path (removes ".pdf" too)

            with open(csv_name, 'w', newline='') as csvfile:
                nounwriter = csv.writer(csvfile)
                nounwriter.writerow([docInfo.title, docInfo.author]) # can add more attributes too
                nounwriter.writerow(["Unique nouns: " + str(unqNouns), " Total nouns: " + str(sumNouns)])
                nounwriter.writerow([totalTimeStr, costPerNounStr])
                for noun in total_nouns:
                    nounwriter.writerow([noun.text, noun.context_sentences, noun.noun_phrases, noun.num_occur])
                print('Data has been successfully saved to ' + csv_name)

