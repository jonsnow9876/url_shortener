from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from starlette.datastructures import URLPath
from sqlalchemy 

import  base62

app = FastAPI()


class URLRequest(BaseModel):
    long_url = HttpUrl


@app.post("/shorten")
async def create_short_url(payload : URLRequest):


@app.get("/{short_code}")
async def redirect_to_url(short_code : str):

