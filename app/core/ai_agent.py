from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.config.settings import settings

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(model=llm_id)

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create agent without state_modifier
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Start conversation with system + user messages
    messages = [SystemMessage(content=system_prompt)]
    for q in query:
        messages.append(HumanMessage(content=q))

    state = {"messages": messages}

    response = agent.invoke(state)

    messages = response.get("messages", [])
    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]

    return ai_messages[-1] if ai_messages else "No response generated"
