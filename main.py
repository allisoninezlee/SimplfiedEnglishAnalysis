import argparse
import os
from os import path
import sentence_parser
import pdfplumber

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
    pdf = sentence_parser.open_pdf(file_path)
    text = sentence_parser.extract_text(pdf)
    sentence_parser.get_sentences(text)