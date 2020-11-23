import spacy

'''''''''''''''''''''''''''''''''''''''''''''''''''
function: get_tokens

description: gets all the nouns within a sentence
and keeps track of the sentences that they are in

parameters: sentences, a list of span objects

returns: a dictionary of noun-sentence pairs
'''''''''''''''''''''''''''''''''''''''''''''''''''
def get_nouns(sentences):
    nouns_dict = {}
    #nlp = spacy.load("en_core_web_sm")

    for sentence in sentences: 
        for token in sentence:
            if token.pos_ == 'NOUN':
                if token.text in nouns_dict:
                    # if it is in the dictionary already, simply add the sentence
                    nouns_dict[token.text].append(sentence)
                else:
                    nouns_dict[token.text] = [sentence]

    return nouns_dict
