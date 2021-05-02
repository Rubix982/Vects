#!/usr/bin/env python3

# Local imports
from src.VectorSpaceModel import VectorSpaceModel

# Package imports
import nltk

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, EmailStr

app = FastAPI()

nltk.download("wordnet")

VSM = VectorSpaceModel()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://vectors.vercel.app/",
    "https://vects.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World"}

@app.get("/query/{query}")
async def get_query_results(query: str) -> dict:
    results = VSM.ComplexQuery(query)
    return {"results": results, "query": query}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None) -> dict:
    return {"item_id": item_id, "q": q}