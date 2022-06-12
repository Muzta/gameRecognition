import multiprocessing
import os
import numpy
from youtube_dl import YoutubeDL
import cv2


def imagesGathering(videoLink: str, game: str, lsOfImages: list([int]), delay: int, startTime: int, folder: str):  
    # Save the image of the nth frame of the given video from the list of lsOfImages[n]
    # in the game folder, with a delay according the desired number of images
    vidcap = cv2.VideoCapture(videoLink) 

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    dl = int(delay * fps)
    st = int(startTime * fps)
    delay = [st + (item * dl) for item in lsOfImages] 

    i = 0
    success = True
    
    while success and i < len(lsOfImages):
        vidcap.set(1, delay[i])
        success, image = vidcap.read()
        # image = imutils.resize(image, height=224)
        file_name = game + "_" + str(lsOfImages[i] + 1) + '.jpg'
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        print(f'Image successfully written at {path}')
        i+=1

def chunkImages(maxImages: int, numCPU: int) -> list([list([int])]):
    # Create the list of the image frame indexes each CPU have to work with
    indexes = numpy.arange(maxImages)
    return numpy.array_split(indexes, numCPU)

def parallelImageExtraction(videoLink: str, game: str, numCPU: int, lsOfIndexes: list([int]), maxImages: int, startTime: int, endTime: int, folder: str):
    # Get the video link to work with and parallelizes video images gathering according
    # to the number of CPU
    vd = YoutubeDL({'format':'best[height<=480]'}).extract_info(videoLink, download = False)
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    
    if endTime:
        duration = endTime - startTime
    elif startTime:
        duration = vd['duration'] - startTime
    else:
        duration = vd['duration']

    data = []
    for i in range(numCPU):
        data.append((vd['url'], game, lsOfIndexes[i], duration // maxImages, startTime, folder))

    pool.starmap(imagesGathering, data)
    pool.close()
    pool.join()

def timeToSeconds(time: str):
    time = time.split(':')
    time.reverse()

    seconds = int(''.join(time[0].split()))

    if len(time) > 1:
        minutes = int(''.join(time[1].split()))
        seconds = seconds+minutes*60

    if len(time) > 2:
        hours = int(''.join(time[2].split()))
        seconds = seconds+ 3600*hours
    return int(seconds)

def readLine(line: str, numImages: int, name: str):
    # Extract the game and youtube video link from each line, creting a the 
    # folder of the game if not exists 
    currentLine = line.split(',')
    game = ''.join(currentLine[0])
    game = game.replace(" ", "_")
    videoLink = ''.join(currentLine[1].split())
    startMoment = None
    endMoment = None

    if len(currentLine)>2:
        startMoment = ''.join(currentLine[2].split())
        startMoment = timeToSeconds(startMoment)

    if len(currentLine)>3:
        endMoment = ''.join(currentLine[3].split())
        endMoment = timeToSeconds(endMoment)

    numCPU = multiprocessing.cpu_count()

    lsOfIndexes = chunkImages(numImages, numCPU)
    folder = os.path.join(os.getcwd(),'datasets',name,game)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    parallelImageExtraction(videoLink, game, numCPU, lsOfIndexes, numImages, startMoment, endMoment, folder)