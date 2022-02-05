import multiprocessing
import os
from extractImages import functions


if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

    with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
        
        for line in f:
            functions.readLine(line, 20)
    