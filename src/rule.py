class Rule:
    def __init__(self, data, min_cases):
        self.terms = {}
        self.cases_covered = data
        self.min_cases = min_cases

    def can_add_term(self, term):
        return term.feature not in self.terms and self.get_cases_covered(term).shape[0] >= self.min_cases

    def add(self, term):
        self.terms[term.feature] = term.value
        self.cases_covered = self.get_cases_covered(term)

    def get_cases_covered(self, term):
        return self.cases_covered.loc[self.cases_covered.iloc[:, term.feature] == term.value]

    def get_label(self):
        return self.cases_covered.index.value_counts().index[0]

