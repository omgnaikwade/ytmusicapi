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
