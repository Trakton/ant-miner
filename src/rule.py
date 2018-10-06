class Rule:
    def __init__(self):
        self.terms = {}
        self.label = 0

    def add(self, term):
        self.terms[term.feature] = term.value

    def cases_covered(self, data):
        
