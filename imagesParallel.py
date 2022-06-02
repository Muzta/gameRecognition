import multiprocessing
import os
from extractImages import functions


if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

    with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
        
        lines = f.read().splitlines()

        for i in range(len(lines)):
            functions.readLine(lines[i], i)
        # for line in f:
        #     functions.readLine(line)