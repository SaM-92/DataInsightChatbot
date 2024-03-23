import streamlit as st
from langchain.chains import LLMChain, SimpleSequentialChain
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


# Check current working directory.
print("Current Working Directory: ", os.getcwd())

# If needed, change it to the directory where your database file is located
# os.chdir("./data")
print("New Working Directory: ", os.getcwd())

db = SQLDatabase.from_uri("sqlite:///eirgrid_data.db")

# db = SQLDatabase.from_uri("sqlite:///eirgrid_data.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# results = db.run("SELECT * FROM energy_data LIMIT 10;")
# try:
#     print(results)
# except TypeError:
#     print("The query result is not directly iterable. Check the method's return type.")


st.title("👨‍💻 Chat with Irish Power System Data")

st.write("Please ask your question.")

# # data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")


# #llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
db = SQLDatabase.from_uri("sqlite:///eirgrid_data.db")
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
response_1 = agent_executor.invoke(query)
st.write(response_1)


# chain1=agent
# chain2 = LLMChain(llm=llm, prompt= prompt3)

# chain_Final = SimpleSequentialChain ( chains=[chain1, chain2] , verbose=True)
