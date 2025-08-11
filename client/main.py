from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent.graphs import workflow


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=Path(__file__).parent.absolute() / "templates"
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request=request, name="index.html"
        )


@app.get("/search_candidate", summary="What kind of developer do you need?")
async def get_candidates(user_prompt: str = Query(
                    description="A detailed description of the developer role you are looking for",
                    min_length=10,
                    example="I need a Python developer with experience in Django, REST APIs, and a good understanding of database design."
                )):

    workflow.invoke({ "messages": [{ "role": "user", "content": user_prompt }], "query": None})
    return {"user": "the usre to be used"}


