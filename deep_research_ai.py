import os
import time
import random
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Set API Keys
os.environ["TAVILY_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

# Define the LangChain LLM model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", max_retries=5)

# Tool: Tavily Search
tavily_tool = TavilySearchResults()
research_tool = Tool(
    name="Tavily Search",
    func=tavily_tool.run,
    description="Searches the web for relevant information about a topic."
)

# ✅ Define state schema using TypedDict
class GraphState(TypedDict):
    user_input: str
    research_data: str
    final_answer: str

# --- Agent Functions ---
def call_openai_with_retry(prompt: str, max_retries: int = 5, initial_delay: int = 1):
    """Calls the OpenAI API with exponential backoff and retry."""
    retries = 0
    while retries < max_retries:
        try:
            response = llm.invoke(prompt)
            return response
        except Exception as e:
            if "RateLimitError" in str(e) or "429" in str(e):
                retries += 1
                delay = initial_delay * (2 ** retries) + random.uniform(1,2)
                print(f"[OpenAI Retry] Rate limit encountered. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"An unexpected error occurred: {e}")  # Log other errors
                raise  # Re-raise other exceptions
    raise Exception(f"Failed to call OpenAI API after {max_retries} retries due to rate limiting or other errors.")

def research_agent(state: GraphState) -> GraphState:
    query = state["user_input"]
    print(f"[Research Agent] Searching for: {query}")
    try:
        search_results = tavily_tool.run(query)
        return {
            "user_input": query,
            "research_data": search_results,
            "final_answer": ""
        }
    except Exception as e:
        print(f"[Research Agent] Error during Tavily search: {e}")
        return {
            "user_input": query,
            "research_data": "Error occurred during web search.",
            "final_answer": "An error occurred while trying to retrieve information."
        }

def answer_agent(state: GraphState) -> GraphState:
    context = state["research_data"]
    print("[Answer Agent] Generating answer from context...")
    if "Error occurred" in context:
        return {
            "user_input": state["user_input"],
            "research_data": context,
            "final_answer": "Could not generate a final answer due to issues during the information retrieval step."
        }
    prompt = f"""
    You are an AI assistant tasked with writing a detailed, well-structured answer
    based on the following web research results:

    {context}

    Write a clean, professional summary of this information.
    """
    try:
        response = call_openai_with_retry(prompt)
        return {
            "user_input": state["user_input"],
            "research_data": context,
            "final_answer": response
        }
    except Exception as e:
        print(f"[Answer Agent] Error generating answer: {e}")
        return {
            "user_input": state["user_input"],
            "research_data": context,
            "final_answer": "An error occurred while generating the final answer."
        }

# --- StateGraph Setup ---
graph_builder = StateGraph(GraphState)  # ✅ Fix here
graph_builder.add_node("research_agent", research_agent)
graph_builder.add_node("answer_agent", answer_agent)

graph_builder.set_entry_point("research_agent")
graph_builder.add_edge("research_agent", "answer_agent")
graph_builder.add_edge("answer_agent", END)

graph = graph_builder.compile()

# --- Execution ---
if __name__ == "__main__":
    user_question = input("Enter your research query: ")
    result = graph.invoke({"user_input": user_question})
    print("\n=== Final Answer ===")
    print(result["final_answer"])