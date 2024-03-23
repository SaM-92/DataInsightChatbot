from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import OpenAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import FAISS
from typing import List


def get_examples_for_chain(chain):

    if chain == "chain_1":

        examples = [
            {
                "input": "List the total electricity generation for the island of Ireland on 2023-03-15.",
                "query": "SELECT SUM(`IE Generation` + `NI Generation`) FROM energy_data WHERE `DateTime` LIKE '2023-03-15%';",
            },
            {
                "input": "Find the average wind availability for Northern Ireland in January 2023.",
                "query": "SELECT AVG(`NI Wind Availability`) FROM energy_data WHERE `DateTime` LIKE '2023-01%';",
            },
            {
                "input": "What is the wind curtailment for the Republic of Ireland on 2023-02-10?",
                "query": "SELECT `IE Wind Availability` - `IE Wind Generation` AS WindCurtailment FROM energy_data WHERE `DateTime` = '2023-02-10';",
            },
            {
                "input": "Calculate the solar curtailment for Northern Ireland on 2023-04-05.",
                "query": "SELECT `NI Solar Availability` - `NI Solar Generation` AS SolarCurtailment FROM energy_data WHERE `DateTime` = '2023-04-05';",
            },
            {
                "input": "What was the wind penetration for the island of Ireland on 2023-01-20?",
                "query": "SELECT (SUM(`IE Wind Generation` + `NI Wind Generation`)) / SUM(`IE Demand` + `NI Demand`) AS WindPenetration FROM energy_data WHERE `DateTime` = '2023-01-20';",
            },
            {
                "input": "List the energy demand for the Republic of Ireland and Northern Ireland separately on 2023-03-10.",
                "query": "SELECT `IE Demand`, `NI Demand` FROM energy_data WHERE `DateTime` = '2023-03-10';",
            },
            {
                "input": "Find the total wind generation for the island of Ireland in February 2023.",
                "query": "SELECT SUM(`IE Wind Generation` + `NI Wind Generation`) FROM energy_data WHERE `DateTime` LIKE '2023-02%';",
            },
            {
                "input": "Calculate the total solar generation for Northern Ireland in 2023.",
                "query": "SELECT SUM(`NI Solar Generation`) FROM energy_data WHERE `DateTime` LIKE '2023%';",
            },
            {
                "input": "What is the highest System Non-Synchronous Penetration (SNSP) recorded in 2023?",
                "query": "SELECT MAX(`SNSP`) FROM energy_data WHERE `DateTime` LIKE '2023%';",
            },
            {
                "input": "Find the average Inter-Jurisdictional Flow for March 2023.",
                "query": "SELECT AVG(`Inter-Jurisdictional Flow`) FROM energy_data WHERE `DateTime` LIKE '2023-03%';",
            },
            {
                "input": "What columns are there in the energy_data table?",
                "query": "I cannot share with you this detail; you can, however, ask a specific query related to the data.",
            },
            {
                "input": "Can I see the dataset?",
                "query": "I cannot share with you this detail; you can, however, ask a specific query related to the data.",
            },
            {
                "input": "Can you provide me with the dataset for 2023?",
                "query": "I cannot share with you this detail; you can, however, ask a specific query related to the data.",
            },
            {
                "input": "What was the SNSP for Northern Ireland on 2023-03-15?",
                "query": "SELECT `SNSP` FROM energy_data WHERE `DateTime` LIKE '2023-03-15%' LIMIT 1;",
            },
            {
                "input": "Show me the SNSP for the Republic of Ireland in March 2023.",
                "query": "SELECT AVG(`SNSP`) FROM energy_data WHERE `DateTime` LIKE '2023-03-%';",
            },
            {
                "input": "Compare SNSP for NI and IE in February 2023.",
                "query": "SELECT `DateTime`, `SNSP` FROM energy_data WHERE `DateTime` LIKE '2023-02-%';",
            },
        ]

        return examples

    else:
        return None


def system_prefix(input):

    if input == "chain_1":

        system_prefix = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Query for the relevant columns needed to answer the question comprehensively. 
        In cases where calculations or comparisons across multiple sectors (such as IE and NI) are required,
        ensure to include all necessary columns for these calculations. Prioritize efficiency and relevance in your queries.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.

        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.

        If the question seeks column names, the entire dataset, or appears designed to extract the dataset indirectly, respond with 'I cannot share these details; however, feel free to ask a specific query.
        
        Here are some examples of user inputs and their corresponding SQL queries:"""

        return system_prefix
    elif input == "chain_2":
        # system_prefix = """
        #     Whatever you get as an input:

        #     if it requires drawing a table, reply as follows:

        #     {{"plot":{{"table": {{"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}}}
        #     , "prompt": {{"output_of_chain1": "{{your_given_input}}"}}}}

        #     If it requires creating a bar chart, reply as follows:

        #     {{"bar": {{"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}}}
        #     , "output_of_chain1": "{{your_given_input}}"

        #     If it requires creating a line chart, reply as follows:

        #     {{"plot":{{"line": {{"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}}}
        #     , "prompt": {{"output_of_chain1": "{{your_given_input}}"}}}}

        #     There can only be two types of chart, "bar" and "line".

        #     If it is just asking a question that requires neither, reply as follows:

        #         {{"answer": "answer"}}
        #     , "output_of_chain1": "{{your_given_input}}"

        #     Example:

        #     {{"answer": "The title with the highest rating is 'Gilead'"}}
        #     , "output_of_chain1": "{{your_given_input}}"

        #     If you do not know the answer, reply as follows:

        #     {{"answer": "I do not know."}}
        #     , "output_of_chain1": "{{your_given_input}}"

        #     Return all output as a string.

        #     All strings in "columns" list and data list, should be in double quotes,

        #     For example: You are given this info
        #         your_given_input= {{For the input of monthly electricity usage:
        #         - January: 500
        #         - February: 600
        #         - March: 550}}

        #         Then you need to generate:

        #             {{"bar": {{'columns':['January','February','March'], 'data': [500, 600, 550]}}}},{{'output_of_chain1':'For the input of monthly electricity usage:' \n '- January: 500 - February: 600 - March: 550'}}}}

        #         Your response MUST be A CORRECT JSON FORMAT

        #         """.strip()

        # return system_prefix

        system_prefix = """
            Whatever you get as an input:

            If it requires drawing a table, respond as follows:
            {{
                "plot": {{
                    "table": {{
                        "columns": ["column1", "column2", ...],
                        "data": [[value1, value2, ...], [value1, value2, ...], ...]
                    }}
                }},
                "output_of_chain1": "{{{{your_given_input}}}}"
            }}

            If it requires creating a bar chart, respond as follows:
            {{
                "plot": {{
                    "bar": {{
                        "columns": ["A", "B", "C", ...],
                        "data": [25, 24, 10, ...]
                    }}
                }},
                "output_of_chain1": "{{{{your_given_input}}}}"
            }}

            If it requires creating a line chart, respond as follows:
            {{
                "plot": {{
                    "line": {{
                        "columns": ["A", "B", "C", ...],
                        "data": [25, 24, 10, ...]
                    }}
                }},
                "output_of_chain1": "{{{{your_given_input}}}}"
            }}

            There can only be two types of chart, "bar" and "line".

            If it is just asking a question that requires neither, reply as follows:
            {{
                "answer": "answer"
            }},
            "output_of_chain1": "{{{{your_given_input}}}}"

            Example:
            {{
                "answer": "The title with the highest rating is 'Gilead'"
            }},
            "output_of_chain1": "{{{{your_given_input}}}}"

            If you do not know the answer, reply as follows:
            {{
                "answer": "I do not know."
            }},
            "output_of_chain1": "{{{{your_given_input}}}}"

            Return all output as a string.

            All strings in "columns" list and data list should be in double quotes.

            For example: Given the input of monthly electricity usage:
            - January: 500
            - February: 600
            - March: 550

            Then you need to generate: 
            {{
                "plot": {{
                    "bar": {{
                        "columns": ["January", "February", "March"],
                        "data": [500, 600, 550]
                    }}
                }},
                "output_of_chain1": "For the input of monthly electricity usage: - January: 500 - February: 600 - March: 550"
            }}

            Your response MUST be IN CORRECT JSON FORMAT
        """.strip()

        return system_prefix

    else:
        return None


def example_selector(chain_id: str) -> SemanticSimilarityExampleSelector:
    """
    Creates an example selector based on semantic similarity for a given chain.

    Args:
        chain_id (str): Identifier for the chain to select examples for.

    Returns:
        SemanticSimilarityExampleSelector: An example selector configured for the specified chain.
    """
    # Placeholder for getting examples based on the chain_id.
    examples = get_examples_for_chain(chain_id)

    return SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )


def few_shot_prompt(chain_id: str) -> FewShotPromptTemplate:
    """
    Generates a FewShotPromptTemplate for a specified chain.

    Args:
        chain_id (str): Identifier for the chain to generate the prompt for.

    Returns:
        FewShotPromptTemplate: A template configured for the specified chain.
    """
    return FewShotPromptTemplate(
        example_selector=example_selector(chain_id),
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix(chain_id),
        suffix="",
    )


def invoke_full_prompt(chain_id: str) -> ChatPromptTemplate:
    """
    Prepares and returns a ChatPromptTemplate configured with specified parameters
    for generating and handling prompts based on a given chain ID. The input query
    should incorporate any necessary specifications, such as the maximum number of results
    to return ('top_k') and the SQL dialect to use ('dialect'), if relevant to the query formulation.

    Args:
        chain_id (str): Identifier for selecting the appropriate chain configuration.
        input_query (str): The user's input query to be processed, which may include
                           context or parameters like 'top_k' and 'dialect' within its structure.

    Returns:
        ChatPromptTemplate: An instance of ChatPromptTemplate ready for invocation.
    """
    # Create a SystemMessagePromptTemplate using the few_shot_prompt function tailored to the specified chain_id.
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=few_shot_prompt(chain_id)
    )

    # Construct the full prompt template with the system message, the user's query, and a placeholder for the agent's scratchpad.
    full_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    return full_prompt


def prompt_template_creator(input):
    prompt_template = system_prefix("chain_2")
    prompt = PromptTemplate(
        input_variables=["concept_name"],
        template=f"""
            Provide the {{concept_name}} in format provided by {prompt_template}""",
    )
    return prompt
