from fastapi import FastAPI
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()
yt = YTMusic()

@app.get("/")
def home():
    return {"status": "API chal rahi hai!"}

@app.get("/search")
def search(q: str):
    return yt.search(q)

@app.get("/stream")
def get_stream_url(q: str):
    # Pehle ytmusicapi se videoId nikalo
    search_results = yt.search(q, filter="songs")
    if not search_results:
        return {"error": "Song nahi mila"}
    
    video_id = search_results[0]['videoId']
    watch_url = f"https://music.youtube.com/watch?v={video_id}"

    # Ab yt-dlp se direct audio URL nikalo
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(watch_url, download=False)
            audio_url = info.get('url', None)
            
            return {
                "title": search_results[0]['title'],
                "videoId": video_id,
                "watch_url": watch_url,
                "direct_audio_url": audio_url  # Yeh asli MP3/Audio link hai
            }
    except Exception as e:
        return {"error": str(e)}
