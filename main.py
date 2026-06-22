from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import HTTPException
from starlette.responses import RedirectResponse
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


class URLRequest(BaseModel):
    long_url : HttpUrl


@app.post("/shorten")
async def create_short_url(short_code : URLRequest, db : db_dependency):

    db_url = db.query(models.URLModel).filter(models.URLModel.short_code == short_code).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=db_url.long_url)

@app.get("/{short_code}")
async def redirect_to_url(short_code : str,db : db_dependency):
    db_url = models.URLModel(long_url=str(short_code.long_url))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    short_code = encode_62(db_url.id)

    db_url.short_code = short_code
    db.commit()

    return {"short_url": f"http://localhost:8000/{short_code}"}

