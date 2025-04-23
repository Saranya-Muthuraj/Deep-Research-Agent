# 🧠 Deep Research AI Agentic System

This project is an **AI-powered Research Agent System** that automates the process of web research and answer generation using the **LangChain framework**, **Tavily Search API**, and **OpenAI's GPT models**. It leverages a multi-step **StateGraph architecture** to collect online information and generate high-quality summaries in response to a user's query.

---

## 🚀 Features

- 🌐 **Web Search** using Tavily API  
- 🤖 **LLM Answer Generation** using GPT-3.5-turbo  
- 🔁 **Robust Retry Logic** for handling API rate limits  
- 🧱 **Graph-based State Management** using LangGraph  
- 🧪 **Clean modular design** with research and answer agents  

---

## 📦 Dependencies

Make sure to install the required Python packages:

```bash
pip install langchain langgraph openai langchain-community
```
## 🔑Environment Variables

Set your API keys in the environment before running the script:

```bash
export TAVILY_API_KEY="your-tavily-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```
Replace the placeholders with your actual API keys.

## 📄 How It Works

1.**User Input**: The user types a query.

2.**Research Agent**: Uses Tavily to search the web for relevant information.

3.**Answer Agent**: Takes the research data and generates a professional answer using OpenAI.

4.**Output**:  Displays the final answer to the user.

## 🧠 Code Overview

## `GraphState`

A custom state schema shared across all nodes of the graph:

```python
class GraphState(TypedDict):
    user_input: str
    research_data: str
    final_answer: str
```
## `research_agent()`

This function handles the web search step using the Tavily tool.

## `answer_agent()`

This step uses OpenAI’s GPT-3.5 to write a clean, structured answer from the research data.

## `call_openai_with_retry()`

Ensures robust communication with the OpenAI API using exponential backoff.

## `StateGraph` Setup

Nodes are added for each agent, and edges define their execution order:

```text
research_agent --> answer_agent --> END
```

## 🧪 Example Usage
```bash
$ python research_agent.py
Enter your research query: latest trends in AI-powered education
```
Output:

```text
=== Final Answer ===
(Generated professional summary based on web results)
```
## 📂 Project Structure

```bash
├── research_agent.py       # Main executable script
├── README.md               # Project documentation
```
## 🛡️ Disclaimer

This tool is for research and educational purposes. Web results may vary based on API limits and content availability.
