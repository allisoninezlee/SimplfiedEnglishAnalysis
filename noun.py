class Noun:

    def __init__(self, text, context_sentence):
        self.text = text   # noun as a string
        self.context_sentences = [context_sentence]   # list of span objects, one for each sentence the noun appears in
        self.num_occur = 1   # number of times the noun has appeared

    # method to be called each time noun appears again after initial object creation
    def add_occur(self, context_sentence):
        self.num_occur += 1
        # check to ensure same sentence will not be listed multiple times
        if context_sentence not in self.context_sentences:
            self.context_sentences.append(context_sentence)
