from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.params import Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from . import models
from .base62 import encode_62
from .database import SessionLocal,engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

app = FastAPI()
app.mount("/static", StaticFiles(directory="url_shortener/static"), name="static")



class URLRequest(BaseModel):
    long_url : HttpUrl

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Force the full path so it finds it every time from the root directory
    with open("url_shortener/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/shorten")
async def create_short_url(payload : URLRequest, db : db_dependency):
    db_url = models.URLModel(long_url=str(payload.long_url))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    generated_code = encode_62(db_url.id)

    db_url.short_code = generated_code
    db.commit()

    return {"short_url": f"http://localhost:8000/{generated_code}"}

@app.get("/{short_code}")
async def redirect_to_url(short_code : str,db : db_dependency):
    # Query the database to find the row matching the incoming string
    db_url = db.query(models.URLModel).filter(models.URLModel.short_code == short_code).first()

    # If it doesn't exist, throw a 404
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Bounce the user's browser to the destination website
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=db_url.long_url)

