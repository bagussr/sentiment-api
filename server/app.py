from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import Sentiment

import os


app = FastAPI(title="Sentimen API")
model = Sentiment()
x = os.path.join(os.getcwd(), "public")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


class Sentiment(BaseModel):
    keyword: list[str]
    title: str


@app.on_event("shutdown")
def shutdown_event():
    for file in os.listdir(x):
        os.remove(os.path.join(x, file))
        print(f"File {file} deleted")


@app.post("/sentiment")
def create_sentiment(data: Sentiment):
    for key in data.keyword:
        model.crawler(key)
    model.getSentiment(data.title)
    return {"data": data}


@app.get("/")
def root():
    return {"message": "Hello World"}
