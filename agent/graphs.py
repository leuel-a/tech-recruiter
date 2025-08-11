from langgraph.graph import StateGraph, START, END
from agent.state_schemas import State

from agent.chains import (
    extract_search_query_from_user_prompt,
    search_candidates_chain,
    rank_candidates_chain
)


graph_builder = StateGraph(State)


graph_builder.add_node("extract_search_query_from_user_prompt", extract_search_query_from_user_prompt)
graph_builder.add_node("search_candidates_from_github", search_candidates_chain)
graph_builder.add_node("rank_candidates_from_github", rank_candidates_chain)

# the steps that the agent will take
graph_builder.add_edge(START, "extract_search_query_from_user_prompt")
graph_builder.add_edge("extract_search_query_from_user_prompt", "search_candidates_from_github")
graph_builder.add_edge("search_candidates_from_github", "rank_candidates_from_github")
graph_builder.add_edge( "rank_candidates_from_github", END)

workflow = graph_builder.compile()
