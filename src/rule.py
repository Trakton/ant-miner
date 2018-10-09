class Rule:
    def __init__(self, data, min_cases):
        self.terms = {}
        self.data = data
        self.min_cases = min_cases
        self.label = None

    def can_add_term(self, term):
        return term.feature not in self.terms and self.get_cases_covered_with_term(term).shape[0] >= self.min_cases

    def add(self, term):
        self.terms[term.feature] = term.value

    def get_cases_covered(self):
        cases_covered = self.data
        for key, value in self.terms.items():
            cases_covered = cases_covered.loc[cases_covered.iloc[:, key] == value]
        return cases_covered

    def get_cases_covered_with_term(self, term):
        cases_covered = self.get_cases_covered()
        return cases_covered.loc[cases_covered.iloc[:, term.feature] == term.value]

    def update_label(self):
        self.label = self.get_cases_covered().index.value_counts().index[0]

    def is_row_covered(self, row):
        for key, value in self.terms.items():
            if(row[key] != value):
                return False
        return True

    def get_quality(self):
        self.update_label()
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
    
    def prune(self):
        while(len(self.terms.keys()) > 1):
            best_q = self.get_quality()
            best_term = None
            for key, value in self.terms.items():
                self.terms.pop(key)
                q = self.get_quality()
                if(q > best_q - 1e-6):
                    best_q = q
                    best_term = key
                self.terms[key] = value

            if(best_term == None):
                break
            
            self.terms.pop(best_term)
        self.update_label()

    def is_equal(self, rule):
        intersection = len(self.terms.items() & rule.terms.items())
        return len(self.terms.items()) == intersection and len(rule.terms.items()) == intersection
