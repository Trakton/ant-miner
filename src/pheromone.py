import numpy as np

class Pheromone:
    def __init__(self, feature_count, values_count):
        self.paths = []
        for i in range(feature_count):
            self.paths.append(np.zeros(values_count[i]))
