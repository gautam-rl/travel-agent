#!/usr/bin/env python

import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.llms import OpenAI
from langchain.agents import AgentExecutor

load_dotenv()

llm = OpenAI(temperature=0)
# tools = load_tools(["serpapi", "llm-math"], llm=llm)

# TODO - we need to teach langchain to use kayak/priceline/tripadvisor API as a tool
tools = load_tools(["llm-math"], llm=llm)

if __name__ == '__main__':
    from langchain.chat_models import ChatOpenAI

    chat_model = ChatOpenAI(temperature=0)

    prompt = hub.pull("hwchase17/react-json")
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    chat_model_with_stop = chat_model.bind(stop=["\nObservation"])

    from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
            }
            | prompt
            | chat_model_with_stop
            | ReActJsonSingleInputOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke(
        {
            "input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
        }
    )
    print("Hello world")
