import googleapiclient.discovery
import vlc
import yt_dlp
import time
import subprocess
import os
import tempfile 
import requests
from ytmusicapi import YTMusic



youtube = googleapiclient.discovery.build(serviceName='youtube', version ='v3', developerKey='AIzaSyAFYl0vjF5pRC3dbS39appi-JXUtfPPAVo')


def searchytmusic():
    return
    

def searchyt(query, max_results=5, page_token=None):
     
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        type='video',
        pageToken= page_token,

    )
    response = request.execute()
    search_response= Search_Response(response)

    return search_response
    


class Search_Response :
    def __init__(self, search_response):
        self.prev= search_response.get('prevPageToken')
        self.next= search_response.get('nextPageToken')

        items= search_response.get('items')

        self.search_results=[]

        for item in items :
            search_result= Search_Result(item)
            self.search_results.append(search_result)


class Search_Result :
    def __init__(self, search_result):
        self.vid_id= search_result['id']['videoId']
        self.title= search_result['snippet']['title']
        self.thumbnail= search_result['snippet']['thumbnails']['default']['url']
        self.channelTitle= search_result['snippet']["channelTitle"]


def display_video(search_response):                                          #Main FUnction in a way

    for i,search_result in enumerate(search_response.search_results) :
        print(f'{i+1}.Video ID: {search_result.vid_id}')
        print(f'Title: {search_result.title}')
        print(f'Channel Title: {search_result.channelTitle}')
        print()
    
    print("Which video do you want to play ?")
    userNum= int(input("Enter the number from list -> ")) -1                   #Choice by user

    if 0<= userNum < len(search_response.search_results):
        video_id= search_response.search_results[userNum].vid_id
        play_video(video_id)
    else :
        print("Title not found in search results")



def play_video(video_id):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'subtitleslangs': ['en'],
    }
    print("In Play function :-")

    url= "https://www.youtube.com/watch?v="+video_id
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=False)
        video_url = video_info['url']

     # Check if 'url' exists in the info dictionary
    if 'url' in video_info:
        video_url = video_info['url']
        # Get subtitles URL if available
        subtitle_url = video_info.get('subtitles', {}).get('en', [{}])[0].get('url')
    else:
        print("Error: URL not found in video info.")
        return  # Exit if the URL is not available

    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"  # Make sure this path is correct
    

    subtitle_path=None

    if subtitle_url:
        subtitle_response= requests.get(subtitle_url)
        
        if subtitle_response.ok:
            subtitle_path= r'C:\Users\saifu\Documents\Subtitles for Python App'
            with open(subtitle_path, 'wb') as f:
                f.write(subtitle_response.content)

    
    vlc_command= [vlc_path, video_url]
    if subtitle_path:
        vlc_command.extend(['--sub-file',subtitle_path])

    try:
        print("VLC Command :", vlc_command)
        subprocess.Popen(vlc_command)
    except Exception as e:
        print(f"Error : {e} Check if path and options correct")
    finally:
        os.remove(subtitle_path)


    #Downloding Video 
    choice= input("Do you want to download the video ?")
    if choice in 'yY':
        download_video(url)
        print("Download finished")
        print("Program End")
    else :
        print("Program End")



def download_audio(url) :
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality':'192',
        }],
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl :
        ydl.download(url)



def download_video(url):
    
    ydl_opts = {
        'format' : 'bestvideo[height>=480]+bestaudio/best',
        'merge_output_format' : 'mp4',
        'outtmpl': r'C:\Users\saifu\Documents\Programs Stuff\Music Player App/downloads/%(uploader)s/%(title)s.%(ext)s',        #Need to add subtitle functionality
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl :
        ydl.download([url])



def download_audio_alt(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': '%(title)s_alt.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

###########################################################################################################################3


query=input("What do you want to watch ? \n")
search_resp= searchyt(query)
display_video(search_resp)
