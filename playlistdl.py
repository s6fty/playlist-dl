import yt_dlp
import configparser
import os
from os import path
import shutil
import musicbrainzngs
import glob
import re
from yt_dlp.postprocessor import MetadataParserPP


#musicbrainzngs.set_useragent("Playlist Downloader - yt-dlp fork", "1", "https://github.com/s6fty")
config = configparser.ConfigParser()

try:
    config.read_file(open('defaults.cfg')) # Try to read config file from same directory

except FileNotFoundError:
    while True:
        formats = ["best" , "mp3", "aac", "opus", "flac", "alac", "wav"] 
        print("Please enter a download directory for files: ")
        directory = input("")
        print("Available formats:")
        print("mp3 (default), aac, m4a, opus, flac, alac, wav, best (experimental)")
        print("Please enter a audio format:")
        audio_format = input("")
        if (audio_format != formats): # If input doesn't match the formats that yt-dlp supports make it mp3
            audio_format = "mp3"
        print("Directory:" + directory)
        print("Audio Format:" + audio_format)
        print("Confirm settings? (y/n)")
        confirm = input("")
        if (confirm == "y"):
            break

    config['CFG'] = {'directory' : directory,
    'audio format' : audio_format} 
    with open('defaults.cfg', 'w') as configfile:
        config.write(configfile)

config.read('defaults.cfg')

print("Please enter a playlist: ")
playlist = input("")

directory = config['CFG']['directory']
audio_format = config['CFG']['audio format']

cwd = os.getcwd() # Get current directory
temp = cwd + '/.tmp' # Create a temporary directory
os.path.exists(temp) or os.mkdir(temp) # If temp directory exist, don't try to create new one, if doesnt create one 




ydl_opts = { 
        'paths' : { "temp" : temp, "home" : directory}, # Adding paths
        'outtmpl': '%(artist)s - %(title)s.%(ext)s', # Filename output
        'overwrites' : 'true',
        'format': audio_format + "/bestaudio/best", # Choose best audio quality for the audio format
        'postprocessors': [{ 'key': 'FFmpegExtractAudio', # mp4 -> mp3
        'preferredcodec': audio_format},
        {'key': 'MetadataParser', # Submit metadata to files for making things easier with MusicBrainz         
        'when': 'pre_process',
        'actions': [(MetadataParserPP.Actions.INTERPRET, 'title', '%(artist)s - %(title)s')]}]
    }

with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
    error_code = ydl.download(playlist) # Finally video starts to download 

# deneme = (cwd + "/deneme/")
# sub_str = " - "
# for music in os.listdir(deneme):
#     filename, extension = path.splitext(music)
#     filename = filename.split(sub_str)
#     qartist = "".join(map(str, filename[0]))                     ## Metadata Fetcher
#     qtitle = "".join(map(str, filename[1]))
#     #print(qtitle,qartist)
#     result = musicbrainzngs.search_releases(artist = qartist, release = qtitle, limit = 5)
#     # for artist in result:
#     print(result)

shutil.rmtree(temp, ignore_errors=False) # Deleting the temp file