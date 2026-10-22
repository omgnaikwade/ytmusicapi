from fastapi import FastAPI
from ytmusicapi import YTMusic

app = FastAPI()
yt = YTMusic()

@app.get("/")
def home():
    return {"status": "API chal rahi hai!"}

@app.get("/search")
def search(q: str):
    return yt.search(q)

# Naya Endpoint: Direct Audio URL nikalne ke liye
@app.get("/stream")
def get_stream_url(q: str):
    # 1. Pehle gaana search karo
    search_results = yt.search(q, filter="songs")
    if not search_results:
        return {"error": "Song nahi mila"}
    
    # 2. Pehle result ki videoId nikaalo
    video_id = search_results[0]['videoId']
    
    # 3. Us videoId se direct stream/audio URL nikaalo
    try:
        watch_playlist = yt.get_watch_playlist(video_id)
        # ytmusicapi stream URL direct nahi deta, par yt-dlp jaisa link 
        # hum ytimg ya direct audio link construct kar sakte hain
        # Yahan hum basic watch URL de rahe hain jise aap play kar sakte hain
        watch_url = f"https://music.youtube.com/watch?v={video_id}"
        
        return {
            "title": search_results[0]['title'],
            "videoId": video_id,
            "watch_url": watch_url,
            "note": "Direct MP3 link ke liye yt-dlp use karna padega, par ye link play ho jayega."
        }
    except Exception as e:
        return {"error": str(e)}
