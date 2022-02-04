import random
import ffmpeg
from youtube_dl import YoutubeDL
import os

# powershell ffmpeg -ss 00:03:22 -i $(youtube-dl -f 22 --get-url https://www.youtube.com/watch?v=4xiRgMuAi3s) 
# -vframes 1 -q:v 2 vayne.jpg
# vd = YoutubeDL({'format':'22'}).extract_info('https://www.youtube.com/watch?v=3D4Tk7oo4e0', download = False)

game = 'leagueoflegends'
videoLink = 'https://www.youtube.com/watch?v=YeGk1vcXR0A'

vd = YoutubeDL({'format':'best'}).extract_info(videoLink, download = False)

for i in range(5):
    {
        ffmpeg
        .input(vd['url'], ss = str(random.randint(0,vd['duration'])) )
        .output(game+str(i)+'.jpg', vframes=1, **{'q:v':2})
        .run()
    }   

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory

# with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
#     for line in f:
#         currentLine = line.split(',')
#         game = ''.join(currentLine[0].split()).lower()
#         videoLink = ''.join(currentLine[1].split())

#         vd = YoutubeDL({'format':'best'}).extract_info(videoLink, download = False)
        
#         for i in range(5)
#             {
#                 ffmpeg
#                 .input(vd['url'], ss=rand(0,vd['duration']))
#                 .output(str(game)+'%d.jpg', vframes=1, **{'q:v':2})
#                 .run()
#             }   