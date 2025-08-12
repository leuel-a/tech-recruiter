from typing import Annotated, Optional, List
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from shared.models import User


class State(TypedDict):
    query: Optional[str]
    search_result_candidates: List[User]
    messages: Annotated[list, add_messages]


