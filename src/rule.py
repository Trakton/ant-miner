class Rule:
    def __init__(self, data, min_cases):
        self.terms = {}
        self.data = data.dataset
        self.min_cases = min_cases

    def get_query(self):
        return ' and '.join(['%s == %s' % (key, value) for (key, value) in self.terms.items()])

    def can_add_term(self, term):
        return term.feature not in self.terms and self.count_cases_covered_with_term(term) >= self.min_cases

    def add(self, term):
        self.terms[term.feature] = term.value

    def get_cases_covered(self):
        return self.data.query(self.get_query())

    def count_cases_covered_with_term(self, term):
        query = '{} == {}'.format(term.feature, term.value)
        if len(self.terms) > 0:
            query = ' and '.join([self.get_query(), query])
        return self.data.query(query).shape[0]

    def get_label(self):
        return self.get_cases_covered().index.value_counts().index[0]

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
        label = self.get_label()
        for index, row in self.data.iterrows():
            if(self.is_row_covered(row)):
                if index == label:
                    tp = tp + 1
                else:
                    fp = fp + 1
            else:
                if index == label:
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

    def is_equal(self, rule):
        intersection = len(self.terms.items() & rule.terms.items())
        return len(self.terms.items()) == intersection and len(rule.terms.items()) == intersection
