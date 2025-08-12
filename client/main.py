from dotenv import load_dotenv
load_dotenv()

import os
import logging
import getpass
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from agent.graphs import workflow
from shared.models import User


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "config.custom_formatter.CustomFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn.error": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}


APP_PORT=os.getenv("APP_PORT", "")
APP_HOST=os.getenv("APP_HOST", "")
APP_LOG_LEVEL=os.getenv("APP_LOG_LEVEL", "")


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


@app.get("/", summary="Home page of the application", response_class=HTMLResponse, tags=["Web Pages"])
async def root(request: Request):
    return templates.TemplateResponse(
            request=request, name="index.html"
        )


@app.get("/search_candidate", summary="What kind of developer do you need?", response_model=List[User], tags=["Candidates"])
async def get_candidates(
            user_prompt: str = Query(
                            description="A detailed description of the developer role you are looking for",
                            min_length=10,
                            examples=["I need a Python developer with experience in Django, REST APIs, and a good understanding of database design."]
                        ),
            location: str = Query(
                            description="The location (Country) of the developer candidate the recruiter wants to search in",
                            examples=["Ethiopia"]
                        )
        ):

    state = await workflow.ainvoke({ "messages": [{ "role": "user", "content": user_prompt + f" located in {location}" }], "query": None, "search_result_candidates": []})

    total_count = state["search_result_candidates"].get("total_count")
    logging.info(f"Search results contain a total of {total_count} candidates")

    candidates = state["search_result_candidates"].get("items", [])
    logging.info(f"The result list contains a total of {len(candidates)} candidates")

    return candidates


if __name__ == '__main__':
    uvicorn.run(
            "client.main:app",
            host=APP_HOST,
            port=int(APP_PORT),
            log_level="info",
            log_config=LOGGING_CONFIG
        )

