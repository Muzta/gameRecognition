import multiprocessing
import os
import numpy
from youtube_dl import YoutubeDL
import cv2

def imagesGathering(vidcap, game, lsOfImages, delay):    
    i = 0
    folder = os.getcwd()
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    
    while success and i < len(lsOfImages):
        success, image = vidcap.read()
        file_name = game + "_" + str(i + 1) + ".jpg"
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image[int(cv2.IMWRITE_JPEG_QUALITY), 100])  #Mejor calidad
        print(f'Image successfully written at {path}')
        vidcap.set(1, delay[i + 1])

def readLine(line):
    currentLine = line.split(',')
    game = ''.join(currentLine[0].split()).lower()
    videoLink = ''.join(currentLine[1].split())

    vd = YoutubeDL({'format':'best'}).extract_info(videoLink, download = False)

    maxImages = 20
    indexes = numpy.arange(maxImages)
    numCPU = multiprocessing.cpu_count()    #   4

    lsOfIndexes = numpy.split(indexes, numCPU)  #   [4*[5]]

    vidcap = cv2.VideoCapture(vd['url'])
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    

    delay = [(item / vd['duration']) * fps for item in lsOfIndexes]

    imagesGathering(vidcap, game, lsOfIndexes, delay)