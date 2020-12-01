# Custom attribute extensions for spaCy containers
from spacy.tokens import Doc, Span, Token

Span.set_extension("document", default = None)    # parent document of the sentence
Span.set_extension("noun_token_objects", default = [])   # list of objects for each noun in the sentence
Span.set_extension("noun_token_text", default = [])    # list of these nouns as strings

Token.set_extension("context_sentences", default = [])   # list of objects for each sentence the noun appears in
Token.set_extension("num_occur", default = 0)   # number of times the noun has appeared
