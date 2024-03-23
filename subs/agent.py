from langchain_community.agent_toolkits import create_sql_agent
from subs.db_connections import connetc_to_irish_db
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
db = connetc_to_irish_db()
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def sql_agent(llm_input, db, prompt):

    agent = create_sql_agent(
        llm=llm_input,
        db=db,
        prompt=prompt,
        verbose=True,
        agent_type="openai-tools",
    )

    return agent
