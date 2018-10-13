import pandas as pd
from data import Data
from ant_miner import AntMiner

def main():
    headers = ['age', 'menopause', 'tumor', 
               'inv', 'node', 'deg', 
               'breast', 'breasttwo', 'irradiant']

    csv = pd.read_csv('../data/breast_cancer.csv', header=None, names=headers, index_col=0)

    data = Data(csv)

    ant_miner = AntMiner(data, 10, 3000, 10, 10)
    ant_miner.fit()

if __name__ == '__main__':
    main()
