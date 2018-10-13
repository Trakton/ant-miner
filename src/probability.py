import numpy as np

def random_pick(probabilities):
    choice = np.random.choice(len(probabilities), 1, p=[x[0] for x in probabilities])[0]
    return probabilities[choice][1]