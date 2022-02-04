import ffmpeg
from youtube_dl import YoutubeDL
import os

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #Current directory
game= "leagueoflegends"
vd = YoutubeDL({'format':'22'}).extract_info("https://www.youtube.com/watch?v=3D4Tk7oo4e0", download = False)
timest = 1 / (vd['duration']//10)

{
    ffmpeg
    .input(vd['url'])
    .output(game+'%d.jpg',**{'q:v':2, 'filter:v': 'fps='+str(timest)})
    .run()
}

# with open(os.path.join(__location__, 'dataset.txt'), 'r') as f:
#     for line in f:
#         currentLine = line.split(',')
#         game = ''.join(currentLine[0].split()).lower()
#         videoLink = ''.join(currentLine[1].split())

#         vd = YoutubeDL().extract_info(videoLink, download = False)
#         print(vd['url'])
#         # timest = 1 / (vd['duration']//10)

#         # {
#         #     ffmpeg
#         #     .input(vd['url'])
#         #     .output('{game}%d.jpeg', **{'q:v':2, 'filter:v': 'fps='+str(timest)})
#         #     .run()
#         # }