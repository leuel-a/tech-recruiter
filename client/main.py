from dotenv import load_dotenv
load_dotenv()

import os
import logging
import getpass
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from agent.graphs import workflow
from shared.models import User
from config.custom_formatter import CustomFormatter


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


app = FastAPI()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API for Google Gemini: ")


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


@app.get("/search_candidate", summary="What kind of developer do you need?", response_model=List[User])
async def get_candidates(
            user_prompt: str = Query(
                            description="A detailed description of the developer role you are looking for",
                            min_length=10,
                            example="I need a Python developer with experience in Django, REST APIs, and a good understanding of database design."
                        ),
            location: str = Query(
                            description="The location (Country) of the developer candidate the recruiter wants to search in",
                            example="Ethiopia"
                        )
        ):

    state = await workflow.ainvoke({ "messages": [{ "role": "user", "content": user_prompt + f" located in {location}" }], "query": None, "search_result_candidates": []})

    # total_count = int(state["search_result_candidates"].get("total_count"))
    candidates = state["search_result_candidates"].get("items", [])

    return candidates


