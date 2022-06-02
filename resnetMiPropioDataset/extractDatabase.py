
import os
from extractImages import functions

DATASETNAME = 'predictDataset'
NIMAGES = 2
LINKSFILEPATH = os.path.join('extractImages','predictVideoLinks.txt')

if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

    with open(os.path.join(__location__, LINKSFILEPATH), 'r') as f:
        
        for line in f:
            functions.readLine(line, NIMAGES, DATASETNAME)

