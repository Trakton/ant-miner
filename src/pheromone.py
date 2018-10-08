import numpy as np

class Pheromone:
    def __init__(self, feature_count, values_count):
        self.paths = []
        for i in range(feature_count):
            self.paths.append(np.full((values_count[i]), 1/sum(values_count)))

    def trail(self, term):
        return self.paths[term.feature][term.value]

    def normalize(self):
        total = 0
        for i in range(len(self.paths)):
            for j in range(len(self.paths[i])):
                total = total + self.paths[i][j]
        
        for i in range(len(self.paths)):
            for j in range(len(self.paths[i])):
                self.paths[i][j] = self.paths[i][j] / total

    def update(self, rule):
        q = rule.get_quality()
        for key, value in  rule.terms.items():
            self.paths[key][value] = self.paths[key][value] + self.paths[key][value] * q
        
        self.normalize()