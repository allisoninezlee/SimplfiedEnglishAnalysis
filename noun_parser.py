import spacy

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: get_tokens

description: gets all the nouns within a sentence

parameters: sentences, a list of span objects

returns: a list of strings reperesenting a page of text
'''''''''''''''''''''''''''''''''''''''''''''''''''
def get_nouns(sentences):
    nouns = []
    #nlp = spacy.load("en_core_web_sm")

    for sentence in sentences: 
        for token in sentence:
            if token.pos_ == 'NOUN':
                print(token)

    return nouns
