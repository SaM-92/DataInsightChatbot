from langchain_community.agent_toolkits import create_sql_agent
from subs.db_connections import connetc_to_irish_db
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from subs.prompts import prompt_template_creator,invoke_full_prompt(chain_id="chain_1")

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

def configure_sequential_chain(chain_id_sql: str = "chain_1", chain_id_response_plot: str = "chain_2") -> SimpleSequentialChain:
    """
    Configures and returns a sequential chain composed of an SQL agent chain and a plot-and-response agent chain.

    Args:
        chain_id_sql (str): The identifier for selecting the appropriate SQL chain configuration.
                            Defaults to "chain_1".
        chain_id_response_plot (str): The identifier for the chain that handles plotting and responses.
                                      Defaults to "chain_2".

    Returns:
        SimpleSequentialChain: A sequential chain that first executes SQL queries and then processes plotting and responses.
    """
    # Invoke the full prompt for the SQL chain using the provided SQL chain ID
    prompt_for_sql = invoke_full_prompt(chain_id=chain_id_sql)
    
    # Create the SQL agent chain with the generated prompt
    chain_sql = sql_agent(prompt=prompt_for_sql)
    
    # Create the plot-and-response agent chain using the provided response and plot chain ID
    chain_response_plot = agent_plot_and_response(chain_id=chain_id_response_plot)
    
    # Combine the SQL agent chain and the plot-and-response agent chain into a sequential chain
    chain_final = SimpleSequentialChain(chains=[chain_sql, chain_response_plot], verbose=True)
    
    # Return the configured sequential chain
    return chain_final