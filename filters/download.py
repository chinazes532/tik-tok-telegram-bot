import requests
from config import api

def download(url):
    api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    payload = {
        "url": url,
        "hd": "1"
    }
    headers = {
        "x-rapidapi-key": api,
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    response = requests.post(api_url, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'play' in data['data']:
            return data['data']['play']
    else:
        print("Failed to fetch video")

    return None