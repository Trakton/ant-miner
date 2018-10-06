import pandas as pd
from pheromone import Pheromone
from rule import Rule
from term import Term

class AntMiner:
    def __init__(self, data, max_uncovered_cases, ant_count, rules_converg_count, min_cases):
        self.data = data
        self.max_uncovered_cases = max_uncovered_cases
        self.ant_count = ant_count
        self.rules_converg_count = rules_converg_count
        self.min_cases = min_cases
        self.feature_count = self.data.shape[1]
        self.value_counts = data.apply(pd.Series.nunique)

    def build_rule(self, pheromone):
        rule = Rule()

        rule.add(Term(3, 5))

        return rule

    def fit(self):
        training_set = range(self.data.shape[0])
        training_set_size = len(training_set)

        discovered_rule_list = []

        while training_set_size > self.max_uncovered_cases:
            t = 0
            j = 0
            pheromone = Pheromone(self.feature_count, self.value_counts)

            while t < self.ant_count and j < self.rules_converg_count:
                rule = self.build_rule(pheromone)
                print(rule.terms)
                t = t + 1

            training_set_size = training_set_size - 1
