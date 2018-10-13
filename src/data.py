import pandas as pd
from term import Term

class Data:
    def encode(self, dataset):
        for column in dataset:
            dataset[column] = pd.Categorical(dataset[column]).codes
        return dataset
    
    def build_terms(self):
        for feature, values in self.feature_options.items():
            for value in range(values):
                self.terms.append(Term(feature, value))
    
    def build_feature_options(self):
        value_counts = self.dataset.apply(pd.Series.nunique)
        for i in range(len(self.features)):
            self.feature_options[self.features[i]] = value_counts[i]


    def __init__(self, dataset):
        self.dataset = self.encode(dataset)
        self.features = list(self.dataset)
        self.feature_options = {}
        self.terms = []
        self.build_feature_options()
        self.build_terms()        
         
        