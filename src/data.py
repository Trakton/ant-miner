import pandas as pd

class Data:
    def encode(self, dataset):
        for column in dataset:
            dataset[column] = pd.Categorical(dataset[column]).codes
        return dataset

    def __init__(self, dataset):
        self.dataset = self.encode(dataset)
        