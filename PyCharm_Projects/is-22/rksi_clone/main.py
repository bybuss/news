from typing import Optional

import aiofiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, q: Optional[str] = None):
    with open("content/news/news.json", encoding="utf-8") as f:
        news_list = json.load(f)

    if q:  # Если запрос не пустой, фильтруйте новости
        news_list = [news for news in news_list if q.lower() in news["title"].lower()]

    return templates.TemplateResponse("index.html", {"request": request, "news_list": news_list, "query": q})

@app.get("/news/{news_id}", response_class=HTMLResponse)
def news_detail(request: Request, news_id: int):
    with open("content/news/news.json", encoding="utf-8") as f:
        news_list = json.load(f)
    news_item = next(filter(lambda x: x['id'] == news_id, news_list), None)
    if news_item is not None:
        return templates.TemplateResponse("news.html", {"request": request, "news_item": news_item})
    else:
        return HTMLResponse(content="Новость не найдена", status_code=404)
