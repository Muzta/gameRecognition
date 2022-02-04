import ffmpeg
from youtube_dl import YoutubeDL

# powershell ffmpeg -ss 00:03:22 -i $(youtube-dl -f 22 --get-url https://www.youtube.com/watch?v=4xiRgMuAi3s) 
# -vframes 1 -q:v 2 vayne.jpg

r = YoutubeDL({'format':'best'}).extract_info('https://www.youtube.com/watch?v=YeGk1vcXR0A', download = False)
duration = r['duration']

{
    ffmpeg
    .input(r['url'], ss="00:03:22")
    .output('testv2i.png',vframes=1, **{'q:v': 2})
    .run()
}

# {
#     ffmpeg
#     .input(r['url'], ss="00:03:22")
#     .output('testv2i.png',vframes=1, **{'q:v': 2})
#     .run()
# }