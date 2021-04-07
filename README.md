# alpha_prototype

Update March 31, 2021
This repository will contain all source code for our initial Text Analysis prototype.

## Installation
To download the necessary modules: 
```
pip install -r requirements.txt
```
Then, download the necessary framework:
```
python -m spacy download en_core_web_sm
```
## Example Usage
```
python3 main.py --file data/document.pdf --database  : runs with the database
python3 main.py --file data/document.pdf : runs without the database
```
Current cmd args implemented: 
--file/-f   file for input
--database/-d boolean flag to use the database or not

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
* PyPDF2: https://pypi.org/project/PyPDF2/
```
pip install PyPDF2
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

# Postman Set up
Click Import and choose Raw text.
Paste:

curl --location --request POST 'http://161.35.254.149/uploads' \
--header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' \
--form 'file=@"/path/to/file"'

Click continue.

In the main page, look for "Body", it's in between "Headers" and "Pre-request Script", click "Body".

There will be an existing value and a key. Delete the whole line (When you put your cruisor on the line, the right end of the line will have an "X", click on it).

Put your cruisor on top of the key and there will be a "Text" appearing on the right side of the cell. 

Click "Text", and change it to file.

Click the first cell of the line, type "file".

In the middle cell of the line, there is a "Select files" button, click on it and choose your pdf file(Just in case it crashes the program with other files, it's set with pdf files only).

Before sending it, go to settings in Postman (Usually it's at the top right).

In General, scroll down and turn on the "Allow reading files outisde working directory".

Now you are all set, click send and wait for the response!

After successfully ran the program on the server, it generates an output.

An output will be:

{

    "data": {
        "downloadlink": "http://161.35.254.149/downloads/.....",
        "success": true
    }
    
}

Copy and past the link on a browser to download the csv file. 


# How it works
It is set up with python flask, it uses "/uploads" as the keyword for POST method and "file" as the request file keyword. After running the program on the server, it generates an output link for user to download. The type of file is set to PDF, files other than PDFs are not accepted. 
