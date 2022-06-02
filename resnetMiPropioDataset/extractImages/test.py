import multiprocessing
import numpy

indexes = numpy.arange(8)
numCPU = multiprocessing.cpu_count()

lsOfIndexes = numpy.split(indexes, numCPU)
lsOfIndexes = [item * 2 for item in lsOfIndexes]
print(lsOfIndexes)
