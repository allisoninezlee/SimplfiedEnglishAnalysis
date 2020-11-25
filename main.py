import argparse
import os
from os import path
import parsers

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

    # right now it just puts sentences into an array
    total_sentences = parsers.get_sentences(text)

    # this takes the sentence arrays and puts nouns into a dictionary
    noun_dict = parsers.get_nouns(total_sentences)
    
    print(noun_dict)