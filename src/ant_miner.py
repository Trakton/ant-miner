import pandas as pd
from pheromone import Pheromone
from rule import Rule
from term import Term
from probability import random_pick

class AntMiner:
    def __init__(self, data, max_uncovered_cases, ant_count, rules_converg_count, min_cases):
        self.data = data
        self.max_uncovered_cases = max_uncovered_cases
        self.ant_count = ant_count
        self.rules_converg_count = rules_converg_count
        self.min_cases = min_cases
        self.feature_count = self.data.shape[1]
        self.value_counts = data.apply(pd.Series.nunique)

    def get_term_probabilities(self, rule, pheromone):
        denominator = 0
        for feature in range(self.feature_count):
            for value in range(self.value_counts[feature]):
                    term = Term(feature, value)
                    if rule.can_add_term(term):
                        denominator = denominator + pheromone.trail(term)

        probabilities = []
        terms = []
        for feature in range(self.feature_count):
            for value in range(self.value_counts[feature]):
                term = Term(feature, value)
                if rule.can_add_term(term):
                    probability = pheromone.trail(term) / denominator
                    probabilities.append(probability)
                    terms.append(term)

        return probabilities, terms

    def build_rule(self, pheromone):
        rule = Rule(self.data, self.min_cases)

        probabilities, terms = self.get_term_probabilities(rule, pheromone)
        while len(terms) > 0:
            rule.add(random_pick(terms, probabilities))
            probabilities, terms = self.get_term_probabilities(rule, pheromone)
        
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
                rule.prune()
                pheromone.update(rule)
        
                print(rule.get_quality())
                print(pheromone.paths)


                t = t + 1

            training_set_size = training_set_size - 1
