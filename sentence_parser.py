'''''''''''''''''''''''''''''''''''''''''''''''''''
file: sentence_parser.py

description: handles all methods for parsing the 
document into sentences
'''''''''''''''''''''''''''''''''''''''''''''''''''

import os
from os import path
import pdfplumber
import re
import spacy

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: open_pdf

description: opens a pdf using pdfplumber

parameters: fname, the path to the pdf

returns: a pdf object
'''''''''''''''''''''''''''''''''''''''''''''''''''
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

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: extract_text

description: extracts the text from the pdf

parameters: pdf, a pdf object

returns: a list of strings reperesenting a page of text
'''''''''''''''''''''''''''''''''''''''''''''''''''
def extract_text(pdf):
    page_text = []

    for page in pdf.pages:
        text = page.extract_text().rstrip()
        page_text.append(text)

    return page_text

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: get_sentences

description: parses an array of text into sentences
separated by '.'

parameters: page_text, a list of text

returns: a list of the Span object from the spacy library, 
representing each sentence. 
'''''''''''''''''''''''''''''''''''''''''''''''''''
def get_sentences(page_text):
    total_sentences = []
    nlp = spacy.load('en_core_web_sm')
    for text in page_text:
        # parse text
        about_text = nlp(text)
        sentences = list(about_text.sents)

        # append the span objects to the total_sentences list
        for sentence in sentences:
            if (sentence[-1].text == '.'):
                total_sentences.append(sentence)

    return total_sentences
