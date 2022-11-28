from fastapi import FastAPI
from pydantic import BaseModel

from utils import Sentiment

import uvicorn
import os


app = FastAPI(title="Sentimen API")
model = Sentiment()
x = os.path.join(os.getcwd(), "public")


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


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
