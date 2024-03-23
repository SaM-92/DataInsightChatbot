from langchain_community.agent_toolkits import create_sql_agent
from subs.db_connections import connetc_to_irish_db
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from subs.prompts import prompt_template_creator
from langchain.chains import LLMChain, SimpleSequentialChain


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


def agent_plot_and_response(chain_id: str) -> LLMChain:
    """
    Prepares an LLM chain with a specific prompt template, based on the given chain ID.

    Args:
        chain_id (str): The identifier for selecting the appropriate chain configuration and prompt template.

    Returns:
        LLMChain: An instance of LLMChain configured with the initialized LLM and the generated prompt template.
    """
    llm = init_llm()
    prompt = prompt_template_creator(chain_id)
    agent = LLMChain(llm=llm, prompt=prompt)
    return agent


chain1 = sql_agent(promot1)
chain2 = agent_plot_and_response(input="chain_2")
chain_Final = SimpleSequentialChain(chains=[chain1, chain2], verbose=True)
