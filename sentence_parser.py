'''''''''''''''''''''''''''''''''''''''''''''''''''
file: sentence_parser.py

description: handles all methods for parsing the 
document into sentences
'''''''''''''''''''''''''''''''''''''''''''''''''''

import os
from os import path
import pdfplumber

def open_pdf(fname):
    print("Opening " + fname)

    # check for valid path and extension
    if not path.exists(fname):
        print("File " + fname + " does not exist. Exiting...")
        exit()
    elif not fname.endswith('.pdf'):
        print("File " + fname + " is not a pdf. Exiting...")
        exit()

    # open pdf    
    pdf = pdfplumber.open(fname)
    
    return pdf

def extract_text(pdf):
    for page in pdf.pages:
        print(page.extract_text())
        
#if __name__ == "__main__":
