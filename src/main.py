import pandas as pd
from data import Data
from ant_miner import AntMiner

def main():
    headers = ['age', 'menopause', 'tumor-size', 
               'inv-nodes', 'node-caps', 'deg-malig', 
               'breast', 'breast-quad', 'irradiant']

    csv = pd.read_csv('../data/breast_cancer.csv', header=None, names=headers, index_col=0)

    data = Data(csv).dataset

    ant_miner = AntMiner(data, 285, 1, 1, 1)
    ant_miner.fit()
    
if __name__ == '__main__':
    main()
