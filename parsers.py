'''''''''''''''''''''''''''''''''''''''''''''''''''
file: parser.py

description: handles all methods for parsing the 
document into sentences and nouns
'''''''''''''''''''''''''''''''''''''''''''''''''''

import os
from os import path
import pdfplumber
import re
import spacy
import extensions

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

returns: a list of the Span objects from the spacy library, 
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
            sentence._.document = 'document_1'   # set parent document (hard code until program accepts multiple files)
            if (sentence[-1].text == '.'):
                total_sentences.append(sentence)

    return total_sentences

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: get_nouns

description: gets all the nouns within a sentence
and keeps track of the sentences that they are in

parameters: sentences, a list of span objects

returns: a list of token objects where each token is a unique noun
'''''''''''''''''''''''''''''''''''''''''''''''''''
def get_nouns(sentences):
    total_nouns = []   # list of objects for nouns
    total_nouns_text = []   # list of these nouns as strings
    #nlp = spacy.load("en_core_web_sm")

    for sentence in sentences:
        for token in sentence:
            if token.pos_ == 'NOUN':
                token._.num_occur += 1
                if token.text in total_nouns_text:
                    # if noun has appeared before, simply add this sentence to the noun's context sentences and
                    # increment # of occurrences
                    token._.context_sentences.append(sentence)
                else:
                    # otherwise, append the new noun to the list of noun objects and noun strings,
                    # as well as add the context sentence
                    total_nouns.append(token)
                    total_nouns_text.append(token.text)
                    token._.context_sentences.append(sentence)

                if token.text not in sentence._.noun_token_text:
                    # if sentence object doesn't have this noun in its noun lists yet, then add it to the lists
                    sentence._.noun_token_objects.append(token)
                    sentence._.noun_token_text.append(token.text)

    return total_nouns