import multiprocessing
import os


if __name__ == '__main__':
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

    with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
        pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
        lines = []
        for line in f:
            lines.append(line)
        
        pool.map(readLine, lines)
        pool.close()
        pool.join()