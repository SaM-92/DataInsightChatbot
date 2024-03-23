from langchain_community.agent_toolkits import create_sql_agent
from subs.db_connections import connetc_to_irish_db
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


# Function to initialize the ChatOpenAI model
def init_llm() -> ChatOpenAI:
    """
    Initialize and return a ChatOpenAI language model instance.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class.
    """
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def sql_agent(prompt):
    """
    Creates and returns a SQL agent configured with a language model, database connection,
    and the provided prompt template.

    Args:
        prompt: The prompt template to be used by the SQL agent.

    Returns:
        An instance of the configured SQL agent.
    """
    load_dotenv()
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    # Initialize the language model and database connection
    llm = init_llm()
    db = connetc_to_irish_db()

    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=prompt,
        verbose=True,
        agent_type="openai-tools",
    )
    return agent
