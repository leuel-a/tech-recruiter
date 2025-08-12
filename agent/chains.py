import os
import logging

import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from .state_schemas import State

load_dotenv()

# TODO: for some reason logging does not work when using uvicorn
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

GITHUB_API_URL = os.getenv("GITHUB_API_URL", "NONE")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "NONE")
GITHUB_API_VERSION = os.getenv("GITHUB_API_VERSION", "NONE")
GITHUB_RESULT_PER_PAGE=int(os.getenv("GITHUB_RESULT_PER_PAGE", "NONE"))

## GITHUB REQUEST HEADERS
request_headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": GITHUB_API_VERSION
    }

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

system_template = """
You are an expert at crafting GitHub user search queries for the GitHub Search Endpoint. Convert the user's prompt into a precise search query, extracting and incorporating the following details when provided:

- Frameworks used (e.g., LangChain, LangGraph, React)
- Programming languages (e.g., Python, JavaScript)
- Specific skills or tools (e.g., API, database, AI)
- Location or other user-specific criteria (e.g., bio, name)

Format the query as a single string suitable for the GitHub Search Endpoint, using GitHub's query syntax (e.g., 'language:python langchain in:bio').
Add search query for looking in the bio of the user (e.g., 'language: javascript in:bio in:readme type:user')
Only search for users not organizations, hence add type:user in the search query that you are going to create.
If certain details are missing, omit them without placeholders. If the user's prompt is unrelated to GitHub user search
(e.g., asking about general knowledge like capitals or unrelated topics), return exactly: 'Cannot create search query'.

Output only the GitHub search query string or 'Cannot create search query'.
"""

extract_search_query_from_user_prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{user_prompt}")]
)


def extract_search_query_from_user_chain(state: State):
    """Extracts the search query for GitHub based on the user query

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the search results.
    :rtype: State
    """
    logger.info("Extracting Search Query....")

    user_prompt = state["messages"][-1].content
    prompt = extract_search_query_from_user_prompt_template.invoke({ "user_prompt": user_prompt })

    # call the llm with the custom prompt
    response = model.invoke(prompt)

    if isinstance(response.content, str):
        state["query"] = response.content
    else:
        state["query"] = None

    return state


async def search_candidates_chain(state: State):
    """Searches for potential candidates based on the query.

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the search results.
    :rtype: State
    """
    logger.info("Searching for Candidates...")
    logger.info(f"Using the following search query for github candidate search {state['query']}")

    if not isinstance(state['query'], str):
        logger.error("State['query'] should be a string, recieved type {type(state['query'])}")
    else:
        search_url = f"{GITHUB_API_URL}/search/users?q={state['query']}&per_page={GITHUB_RESULT_PER_PAGE}"
        logger.info(f"GitHub Search URL is {search_url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(search_url, headers=request_headers)
                result_candidates = response.json()
                state["search_result_candidates"] = result_candidates

                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url}.")
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}.")
    return state


def rank_candidates_chain(state: State):
    """Ranks the found candidates based on their relevance to the query.

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the ranked candidates.
    :rtype: State
    """
    logger.info("Ranking Candidates...")
    return state



