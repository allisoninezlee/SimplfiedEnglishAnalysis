import argparse
import os
from os import path
import parsers
import document

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
    document_object = document.Document(pdf)

    # get list of span (sentence) objects - one for each sentence in pdf file
    total_sentences = parsers.get_sentences(text)

    # get list of token (noun) objects
    # Note: we'll need to adjust so that the same noun with different capitalization isn't picked up twice
    #       (airplane vs Airplane)
    total_nouns = parsers.get_nouns(total_sentences)

    for noun in total_nouns:
        print(noun.text)

    # add export to database next