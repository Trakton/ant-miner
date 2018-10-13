import numpy as np

class Pheromone:
    def __init__(self, feature_options):
        total = sum(feature_options.values())
        self.paths = {feature: np.full(n_options, 1/total) for feature, n_options in feature_options.items()}

    def trail(self, term):
        return self.paths[term.feature][term.value]

    def normalize(self):
        total = sum(sum(self.paths[key]) for key in self.paths)
        self.paths = {feature: list(map(lambda v: v/total, values)) for feature, values in self.paths.items()}

    def update(self, rule):
        q = rule.get_quality()
        for key, value in rule.terms.items():
            self.paths[key][value] += self.paths[key][value] * q
        self.normalize()