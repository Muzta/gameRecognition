import multiprocessing
import os
import numpy
from youtube_dl import YoutubeDL
import cv2
import imutils

def imagesGathering(lineNum:int, videoLink: str, game: str, lsOfImages: list([int]), delay: int):  
    # Save the image of the nth frame of the given video from the list of lsOfImages[n]
    # in the game folder, with a delay according the desired number of images
    vidcap = cv2.VideoCapture(videoLink) 
    print("Error")
    print(vidcap.isOpened())
    print(vidcap)
    print(vidcap.read())
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    dl = delay * fps
    delay = [item * dl for item in lsOfImages] 

    i = 0
    folder = os.getcwd() + '/dataset/' + game
    success = True
    
    while success and i < len(lsOfImages):
        vidcap.set(1, delay[i])
        success, image = vidcap.read()
        # image = imutils.resize(image, height=224)
        file_name = str(lineNum) + game + "_" + str(lsOfImages[i] + 1) + '.jpg'
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        print(f'Image successfully written at {path}')
        i+=1

def chunkImages(maxImages: int, numCPU: int) -> list([list([int])]):
    # Create the list of the image frame indexes each CPU have to work with
    indexes = numpy.arange(maxImages)
    return numpy.array_split(indexes, numCPU)

def parallelImageExtraction(lineNum:int, videoLink: str, game: str, numCPU: int, lsOfIndexes: list([int]), maxImages: int):
    # Get the video link to work with and parallelizes video images gathering according
    # to the number of CPU
    vd = YoutubeDL({'format':'best[height<=480]'}).extract_info(videoLink, download = False)
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    print("URL")
    print(vd['url'])
    data = []
    for i in range(numCPU):
        data.append((lineNum, vd['url'], game, lsOfIndexes[i], vd['duration'] // maxImages ))

    pool.starmap(imagesGathering, data)
    pool.close()
    pool.join()

def readLine(line: str, lineNum: int):
    # Extract the game and youtube video link from each line, creting a the 
    # folder of the game if not exists 
    currentLine = line.split(',')
    game = ''.join(currentLine[0])
    game = game.replace(" ", "_")
    videoLink = ''.join(currentLine[1].split())
    try:
        numImages = currentLine[2]
    except IndexError:
        numImages = 10

    numCPU = multiprocessing.cpu_count()

    lsOfIndexes = chunkImages(numImages, numCPU)
    folder = os.getcwd() + '\\dataset\\' + game
    if not os.path.isdir(folder):
        os.makedirs(folder)
    parallelImageExtraction(lineNum, videoLink, game, numCPU, lsOfIndexes, numImages)