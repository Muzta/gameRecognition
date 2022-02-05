import multiprocessing
import os
import numpy
from youtube_dl import YoutubeDL
import cv2

def imagesGathering(videoLink: str, game: str, lsOfImages: list[int], delay: int):  
    # Save the image of the nth frame of the given video from the list of lsOfImages[n]
    # in the game folder, with a delay according the desired number of images
    vidcap = cv2.VideoCapture(videoLink) 

    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    dl = delay * fps
    delay = [item * dl for item in lsOfImages] 

    i = 0
    folder = os.getcwd() + '\\' + game + '\\'
    success = True
    
    while success and i < len(lsOfImages):
        vidcap.set(1, delay[i])
        success, image = vidcap.read()
        file_name = game + "_" + str(lsOfImages[i] + 1) + '.jpg'
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        print(f'Image successfully written at {path}')
        i+=1

def chunkImages(maxImages: int, numCPU: int) -> list[list[int]]:
    # Create the list of the image frame indexes each CPU have to work with
    indexes = numpy.arange(maxImages)
    return numpy.array_split(indexes, numCPU)

def parallelImageExtraction(videoLink: str, game: str, numCPU: int, lsOfIndexes: list[int], maxImages: int):
    # Get the video link to work with and parallelizes video images gathering according
    # to the number of CPU
    vd = YoutubeDL({'format':'best'}).extract_info(videoLink, download = False)
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    data = []
    for i in range(numCPU):
        data.append((vd['url'], game, lsOfIndexes[i], vd['duration'] // maxImages ))

    pool.starmap(imagesGathering, data)
    pool.close()
    pool.join()

def readLine(line: str, maxImages: int):
    # Extract the game and youtube video link from each line, creting a the 
    # folder of the game if not exists 
    currentLine = line.split(',')
    game = ''.join(currentLine[0].split()).lower()
    videoLink = ''.join(currentLine[1].split())

    numCPU = multiprocessing.cpu_count()

    lsOfIndexes = chunkImages(maxImages, numCPU)
    folder = os.getcwd() + '\\' + game + '_images'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    parallelImageExtraction(videoLink, game, numCPU, lsOfIndexes, maxImages)