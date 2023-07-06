from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests
from bs4 import BeautifulSoup

app = FastAPI()
origins = [
    "https://aki168.github.io/sakeholic/",
    "https://aki168.github.io",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}

class Item(BaseModel):
    name: str
    brewery: str 

@app.post('/get_sake_images')
async def get_img_from_google(item: Item):
    keyword = item.name + " " + item.brewery
    web = requests.get("https://www.google.com/search?q={}&tbm=isch&gl=jp&hl=ja".format(keyword))
    soup = BeautifulSoup(web.text, "html.parser")
    pics = soup.find_all("img")
    image_path = []
    for i in pics:
        if "images?" in i['src'] :
            image_path.append(i['src'])
    return {'res': image_path[:4], 'version': __version__, "time": time()}
