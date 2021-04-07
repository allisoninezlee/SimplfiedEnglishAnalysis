class Noun:

    def __init__(self, text, context_sentence):
        self.text = text   # noun as a string
        self.context_sentences = [context_sentence]   # list of span objects, one for each sentence the noun appears in
        self.noun_phrases = []
        self.num_occur = 1   # number of times the noun has appeared

    # method to be called each time noun appears again after initial object creation
    def add_occur(self, context_sentence):
        self.num_occur += 1
        if context_sentence not in self.context_sentences:   # checks to ensure same sentence will not be listed multiple times
            self.context_sentences.append(context_sentence)

    def add_phrase(self, noun_phrase):
        if noun_phrase not in self.noun_phrases:   # checks to ensure same phrase will not be listed multiple times
            self.noun_phrases.append(noun_phrase)