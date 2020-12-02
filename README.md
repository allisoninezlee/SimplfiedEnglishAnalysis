# alpha_prototype

This repository will contain all source code for our initial Text Analysis prototype.

## Example Usage
```
python3 main.py --file data/document.pdf
```
Current cmd args implemented: 
--file/-f   file for input

## Module list:
* pdfplumber:
https://github.com/jsvine/pdfplumber
```
pip install pdfplumber
```
* spacy: https://spacy.io/
```
pip install spacy 
python -m spacy download en_core_web_sm
```
* mysql.connector:
https://dev.mysql.com/doc/connector-python/en/
```
pip install mysql-connector-python
```

## Explanation of Internal Data Structures:
We will be creating objects out of our own classes, as well as the 3 types of containers spaCy includes: Doc, Span, 
and Token. Below is a summary of the data structures and where to find any spaCy documentation on them:

Document objects will be used to store information about the document(s) the user uploads. This includes the document's
name, its publication year, the product it is written about, its location, and a list of sentence/span objects found
in this document. 
(See document.py file for more info)

A Doc container is a way to store a block of text and perform operations on it. Our program will create a Doc
object for each page of text from the PDF the user uploads. 
https://spacy.io/api/doc

The block of text in the Doc object can then be divided into smaller parts, called Spans. Our program will create a 
Span object for each sentence found in the block of text. Spans store the sentence as a string, the main document the
sentence came from, the Doc (page) the sentence came from, a list of the objects created for nouns in the sentence, and
a list of the nouns as strings (to make comparing the nouns easier/more time efficient)
https://spacy.io/api/span

The Span objects can be divided into Tokens. While parsing, a Token object will be created for each word in the
sentence. 
https://spacy.io/api/token

Tokens will then be analyzed to determine if they are a noun or not. If the token is a noun, a noun object will
be created for that specific noun. Each noun object has the word stored as a string, the number of times it has 
appeared, and a list of Span objects - one for each sentence the noun appears in.
(See noun.py file for more info)

# Installing programs for MySQL:
Visit https://dev.mysql.com/downloads/ and download the following:
* MySQL Community Server
* MySQL Workbench
* Connector/Python