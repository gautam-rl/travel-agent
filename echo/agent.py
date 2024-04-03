#!/usr/bin/env python

from typing import Any, Dict
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
import runloop

class Agent:
    """
    Sets up a langchain using a travel planner agent, that has access to a search tool and a summarizer tool.
    """
    _agent_executor : AgentExecutor

    def __init__(self):
        # DuckDuckGo search tool
        ddg_search = DuckDuckGoSearchResults()

        # Summarizer tool
        summarize_template = "Summarize the following content: {content}"
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        #llm = ChatOpenAI(model="gpt-3.5-turbo")
        llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(summarize_template)
        )
        summarize_tool = Tool.from_function(
            func=llm_chain.run,
            name="Summarizer",
            description="Summarizes a web page"
        )

        # Web fetch tool
        web_fetch_tool = Tool.from_function(
            func=fetch_web_page,
            name="WebFetcher",
            description="Fetches the content of a web page"
        )

        # Create a REACT agent with access to tools.
        #tools = [ddg_search, web_fetch_tool, summarize_tool]
        tools = [ddg_search, summarize_tool]
        #tools = [summarize_tool]

        # TODO - structure the prompt
        prompt = PromptTemplate.from_template(
            """
            Answer the following questions as best you can. You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action, e.g. the search query
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}
            """)
        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )

        self._agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True) # type: ignore

    def run(self, prompt: str) -> Dict[str, Any]:
        return self._agent_executor.invoke({"input": prompt})


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
}

def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    text_content_with_links = soup.get_text()
    return text_content_with_links


# TODO - this breaks langchain
#@runloop.function
def fetch_web_page(url: str) -> str:
    # Check if valid url
    if not url.startswith("http"):
        return "Invalid URL"
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)


@runloop.function
def plan_trip(prompt: str) -> str:
    result: Dict[str, Any]
    with get_openai_callback() as cb:
        result = agent.run(prompt)
        print(f"OpenAI Usage:\n{cb}")
    return result["output"]


load_dotenv()
agent = Agent()


if __name__ == '__main__':
    # Just run an example
    prompt = "I want to travel somewhere warm in January for 1 week. My home airport is SFO. Do research on my behalf and present me with 3 detailed itineraries that are self contained."
    # Use your tools to search and summarize content into a guide on how to use the requests library."
    print(agent.run(prompt))
