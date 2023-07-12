from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
# from recommendation_system import find_similar_sake

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
        <script src="https://cdn.tailwindcss.com"></script>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
    <main class="container mx-auto divide-y divide-gray-400 divide-dotted py-5">
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg h-80">
            <h1 class="font-light text-3xl align-middle mb-2">SAKEHOLIC API DOC</h1>
            <ul>
                <li><a class="text-red-900 hover:text-red-700 font-bold" href="/docs">/docs</a></li>
                <li><a class="text-red-900 hover:text-red-700 font-bold" href="/redoc">/redoc</a></li>
            </ul>
        </div>
    </main>
    </body>
</html>
"""


@app.get("/")
async def root():
    return HTMLResponse(html)

class Item(BaseModel):
    name: str
    brewery: str

class Sake(BaseModel):
    sid: str

@app.post('/get_sake_images')
async def get_img_from_google(item: Item):
    keyword = item.name + " " + item.brewery
    web = requests.get("https://www.google.com/search?q={}&tbm=isch&gl=jp&hl=ja".format(keyword))
    soup = BeautifulSoup(web.text, "html.parser")
    pics = soup.find_all("img")
    image_path = []
    for i in pics:
        if "images?" in i['src']:
            image_path.append(i['src'])
    return {'res': image_path[:4], 'version': __version__, "time": time()}

# @app.post('/get_similar_sake')
# async def get_similar_sake(sake:Sake):
#     result = find_similar_sake(sake.sid)
#     if result:
#         return {'res': jsonable_encoder(result), 'version': __version__, "time": time()}
#     else:
#         return {'res': None, 'version': __version__, "time": time()}

# @app.post('/get_brewery_info')
# async def get_info_from_google(item:Item):
#     keyword = item.name+ " " +item.brewery
#     web = requests.get("https://www.google.com/search?q={}&gl=jp&hl=ja".format(keyword))
#     soup = BeautifulSoup(web.text, "html.parser")
#     headings = soup.find_all("h3")
#     for title in headings:
#         print(title+"\n")
