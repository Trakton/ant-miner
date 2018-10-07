import numpy as np

class Pheromone:
    def __init__(self, feature_count, values_count):
        self.paths = []
        for i in range(feature_count):
            self.paths.append(np.full((values_count[i]), 1/sum(values_count)))

    def trail(self, term):
        return self.paths[term.feature][term.value]