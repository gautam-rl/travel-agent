#!/usr/bin/env python

import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI

load_dotenv()

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

if __name__ == '__main__':
    print("Hello world")
