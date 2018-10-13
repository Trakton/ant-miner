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

    def get_term_probabilities(self, rule, pheromone):
        denominator = sum(pheromone.trail(term) for term in self.data.terms if rule.can_add_term(term))
        probabilities = [(pheromone.trail(term) / denominator, term) for term in self.data.terms if rule.can_add_term(term)]
        return probabilities

    def build_rule(self, pheromone):
        rule = Rule(self.data, self.min_cases)
        probabilities = self.get_term_probabilities(rule, pheromone)

        while len(probabilities) > 0:
            rule.add(random_pick(probabilities))
            probabilities = self.get_term_probabilities(rule, pheromone)
        
        return rule

    def fit(self):
        training_set = list(range(self.data.dataset.shape[0]))
        discovered_rule_list = []

        while len(training_set) > self.max_uncovered_cases:
            t = 0
            j = 0
            pheromone = Pheromone(self.data.feature_options)
            previous_rule = Rule(self.data, self.min_cases)
            best_rule = Rule(self.data, self.min_cases)
            best_quality = 0
            while t < self.ant_count and j < self.rules_converg_count:
                rule = self.build_rule(pheromone)
                rule.prune()
                pheromone.update(rule)

                if rule.get_quality() > best_quality:
                    best_rule = rule
                    best_quality = rule.get_quality()

                if rule.is_equal(previous_rule):
                    j = j + 1

                print(rule.terms)
                print(rule.get_quality())

                t = t + 1

            discovered_rule_list.append(best_rule)

            new_training_set = []
            label = best_rule.get_label()
            for i in training_set:
                if (label == self.data.dataset.index[i] and best_rule.is_row_covered(self.data.dataset.iloc[i])) == False:
                    new_training_set.append(i)

            training_set = new_training_set
            print(training_set)
