import random
import webbrowser
import requests
from bs4 import BeautifulSoup
import keyboard
from googleapiclient.discovery import build


# YouTube channel ID

#CHANNEL_ID = 'UCiOs68ArGGWo_eZCsPEVG1Q'
CHANNEL_ID = 'UCI6QcXatdaEAaRTRjl3dc0w'
##

# Google news website URL
NEWS_URL = 'https://www.artificialintelligence-news.com/'

from googleapiclient.discovery import build

#This function obtains the channel id of the YouTube channel
def get_channel_id(api_key, channel_name):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel',
        maxResults=1
    )
    response = request.execute()
    channel_id = response['items'][0]['snippet']['channelId']
    return channel_id

#This function obtains all the short videos of the chosen YouTube channel
def fetch_all_short_videos():
    #MY YOUTUBE API
    api_key='AIzaSyC-hg8pxSBysKaggNPm4a_3OaoAp-5EeZw'
    #CHANNEL ID you can change the channel @picpodtv for another
    channel_id = get_channel_id(api_key, '@PICPODTV')

    youtube = build('youtube', 'v3', developerKey=api_key)

    short_videos = []

    next_page_token = None
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            order='date',  # Order by date to get most recent videos
            maxResults=50,  # Maximum number of results per page
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            # You may need to add additional criteria to filter shorts
            if 'short' in title.lower() or 'short' in description.lower():
                short_videos.append({'video_id': video_id, 'title': title})

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return short_videos




#This function opens a random short video from the chosen YouTube channel
def open_youtube_shorts():
    """
    Opens a random video from the shorts of the specified YouTube channel.
    This function uses the YouTube Data API to fetch the list of shorts from the
    specified channel, selects a random video from the list, and opens it in the
    default web browser.
    """
    print("Creando la lista de todos los videos short... Por favor espere")
    shorts_url=fetch_all_short_videos()
    print("Done!")
    # Check if the API response contains any videos
    if shorts_url != 0:
        random_video = random.choice(shorts_url)
        print("Abriendo video...")
        video_url = f'https://www.youtube.com/shorts/{random_video['video_id']}'
        # Open the selected video in the default web browser
        webbrowser.open(video_url)
        print("Esperando que ingrese un comando: Ctrl+N or Ctrl+Y. Presione Esc para salir.")
        return
    else:
        print("No shorts found for the specified YouTube channel.")
        return

def open_google_news():
    """
    Opens a random article from the Google news website.

    This function fetches the HTML content of the Google news website, parses
    the HTML to extract the article links, selects a random article link, and
    opens it in the default web browser.
    """
    # Fetch the HTML content of the Google news website
    response = requests.get(NEWS_URL)
    html_content = response.content
    
    # Parse the HTML to extract the article links
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print("Creando la lista de todos los articulos. Por favor espere...")
    article_links = [link.get('href') for link in soup.find_all('a', class_='img-link')]
    print("Done!")
    
    # Select a random article link and open it in the default web browser
    if article_links:
        random_article = random.choice(article_links)
        webbrowser.open(random_article)
        print("Esperando que ingrese un comando: Ctrl+N or Ctrl+Y. Presione Esc para salir.")
        return
    else:
        print("No articles found on the Google news website.")
        return



# Register hotkeys
print("Esperando que ingrese un comando: Ctrl+N or Ctrl+Y. Presione Esc para salir.")
keyboard.add_hotkey('ctrl+y', open_youtube_shorts)
keyboard.add_hotkey('ctrl+n', open_google_news)
# Keep the script running
keyboard.wait('esc')





