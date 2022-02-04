import cv2
from youtube_dl import YoutubeDL
import os

def imagesGathering(video, duration, game, max_images, silent=False):    
    vidcap = cv2.VideoCapture(video)
    count = 0
    num_images = 0
    folder = os.getcwd()
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    delay = duration // max_images
    
    while success and num_images < max_images:
        success, image = vidcap.read()
        num_images += 1
        file_name = game + "_" + str(num_images) + ".jpg"
        path = os.path.join(folder, file_name)
        cv2.imwrite(path, image)
        print(f'Image successfully written at {path}')
        count += delay*fps
        vidcap.set(1, count)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
    for line in f:
        currentLine = line.split(',')
        game = ''.join(currentLine[0].split()).lower()
        videoLink = ''.join(currentLine[1].split())

        vd = YoutubeDL({'format':'best'}).extract_info(videoLink, download = False)
        imagesGathering(vd['url'], vd['duration'], game, 20, silent=False)


# while success and i < 5:
#     success, image = vidcap.read()
#     file_name = "\ " + game + str(i) + ".jpg"
#     direc = path + file_name
#     cv2.imwrite(direc, image)
#     if cv2.imread(path) is None:
#         os.remove(path)
#     count += 30*fps
#     vidcap.set(1, count)