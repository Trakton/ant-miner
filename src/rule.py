class Rule:
    def __init__(self, data, min_cases):
        self.terms = {}
        self.cases_covered = data
        self.data = data
        self.min_cases = min_cases
        self.label = None

    def can_add_term(self, term):
        return term.feature not in self.terms and self.get_cases_covered(term).shape[0] >= self.min_cases

    def add(self, term):
        self.terms[term.feature] = term.value
        self.cases_covered = self.get_cases_covered(term)
        self.update_label()

    def get_cases_covered(self, term):
        return self.cases_covered.loc[self.cases_covered.iloc[:, term.feature] == term.value]

    def update_label(self):
        self.label = self.cases_covered.index.value_counts().index[0]

    def is_row_covered(self, row):
        for key, value in self.terms.items():
            if(row[key] != value):
                return False
        return True

    def get_quality(self):
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for index, row in self.data.iterrows():
            if(self.is_row_covered(row)):
                if index == self.label:
                    tp = tp + 1
                else:
                    fp = fp + 1
            else:
                if index == self.label:
                    fn = fn + 1
                else:
                    tn = tn + 1
        return (tp/(tp+fn))*(tn/(fp+tn))


