#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool, DuckDuckGoSearchResults
import runloop
from langchain_openai import ChatOpenAI

class Agent:
    """
    Sets up a langchain using a travel planner agent, that has access to a search tool and a summarizer tool.
    """
    _agent : AgentExecutor = None

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

        #tools = [ddg_search, web_fetch_tool, summarize_tool]
        tools = [ddg_search, summarize_tool]

        self._agent = initialize_agent(
            tools=tools,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            llm=llm,
            verbose=True,
            handle_parsing_errors=True,
        )

    def run(self, prompt: str) -> str:
        return self._agent.run(prompt)


load_dotenv()
agent = Agent()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
}

def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    text_content_with_links = soup.get_text()
    return text_content_with_links


@runloop.function
def fetch_web_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)


web_fetch_tool = Tool.from_function(
    func=fetch_web_page,
    name="WebFetcher",
    description="Fetches the content of a web page"
)

@runloop.function
def plan_trip(prompt: str) -> str:
    return agent.run(prompt)

if __name__ == '__main__':
    # Just run an example
    prompt = "I want to travel somewhere warm in January for 1 week. My home airport is SFO. Do research on my behalf and present me with 3 detailed itineraries that are self contained." # Use your tools to search and summarize content into a guide on how to use the requests library."
    print(agent.run(prompt))
