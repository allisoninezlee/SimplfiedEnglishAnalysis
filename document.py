class Document:

    def __init__(self, pdf, document_name, pub_year, product, location):
        self.pdf = pdf
        self.document_name = document_name
        self.pub_year = pub_year
        self.product = product
        self.location = location
        self.sentence_objects = []

