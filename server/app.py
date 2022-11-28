from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils import Sentiment

import os


app = FastAPI(title="Sentimen API")
x = os.path.join(os.getcwd(), "public")

app.mount("/public", StaticFiles(directory="public"), name="public")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


class SentimentSchema(BaseModel):
    keyword: list[str]
    title: str
    limit: int


@app.post("/sentiment")
def create_sentiment(data: SentimentSchema):
    model = Sentiment()
    for key in data.keyword:
        model.crawler(key, data.limit)
    model.getSentiment(data.title)
    return {"data": os.listdir(x)}


@app.get("/")
def root():
    return {"message": "Hello World"}
