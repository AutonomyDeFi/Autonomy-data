import autonomy as a 
import os
from dotenv import load_dotenv

tools = a.tools

from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain_experimental.autonomous_agents import BabyAGI


from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, SerpAPIWrapper, LLMChain
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY", "")
prompt ="You are an AGI agent responsible for providing recommendations on which agent should be used to handle a specific task. Analyze the provided major objective of the project and a single task from the JSON checklist generated by the previous agent, and suggest the most appropriate agent to work on the task."
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

tool_names = [tool.name for tool in tools]

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
    chat_history_memory=FileChatMessageHistory("chat_history.txt"),
)



agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

agent_executor.run(
    input="Swap my Eth to USDC if gas is under $1"
)   