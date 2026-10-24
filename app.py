import uuid

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import string
import random
app = FastAPI()

original_url = {}
def generate_short_code():
    while True:
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        code = ''.join(random.choices(characters, k=6))
        if code not in original_url:
            return code

class URLRequest(BaseModel):
    longurl:str


@app.post('/shorten', status_code=status.HTTP_201_CREATED)
def shorten(request:URLRequest):
    short_code = generate_short_code()
    original_url[short_code] = request.longurl
    return {"short_url": f"localhost:8000/{short_code}"}


@app.get('/{shortcode}')
def hello(shortcode:str):
    if shortcode not in original_url:
        raise HTTPException(status_code=404,detail="URL NOT FOUND")
    return RedirectResponse(original_url[shortcode], status_code=302)

