from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import Sentiment

import os


app = FastAPI(title="Sentimen API")
x = os.path.join(os.getcwd(), "public")


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


@app.on_event("shutdown")
def shutdown_event():
    for file in os.listdir(x):
        os.remove(os.path.join(x, file))
        print(f"File {file} deleted")


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
