#!/usr/bin/env python3

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, EmailStr

from src.BooleanRetrievalModel import BooleanRetrievalModel 


app = FastAPI()

origins = [
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

word_dict = {}

with open('./dist/Total-Words.csv', mode='r') as file:
    for line in file:
        tokens = line.split(',')
        word_dict[tokens[1]] = tokens[0]

class QueryInput(BaseModel):
    query: str


@app.get("/")
def read_root():
    print('hellllo, world!')
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/request/")
async def get_post_items(query: str = ""):
    boolean_query(query)
    print(query)
    return {"Received": "Yayyyy this works!"}
