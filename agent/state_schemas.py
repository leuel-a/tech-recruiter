from typing import Annotated, Optional
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    query: Optional[str]
    messages: Annotated[list, add_messages]


