from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from .state_schemas import State

load_dotenv()

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


def extract_search_query_from_user_prompt(state: State):
    """Extracts the search query for GitHub based on the user query

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the search results.
    :rtype: State
    """
    print("Extracting Search Query....")
    return state


def search_candidates_chain(state: State):
    """Searches for potential candidates based on the query.

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the search results.
    :rtype: State
    """
    print("Searching for Candidates...")
    return state


def rank_candidates_chain(state: State):
    """Ranks the found candidates based on their relevance to the query.

    :param state: The current state of the recruiter agent.
    :type state: State
    :returns: The updated state with the ranked candidates.
    :rtype: State
    """
    print("Ranking Candidates...")
    return state



