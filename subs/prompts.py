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
                "input": "Show me the electricity demand for each hour on 2022-02-02 for both IE and NI.",
                "query": """
                SELECT
                DATE_FORMAT(`DateTime`, '%Y-%m-%d %H:00:00') AS Hour,
                AVG(`IE Demand`) AS `Average IE Demand`,
                AVG(`NI Demand`) AS `Average NI Demand`
                FROM
                energy_data
                WHERE
                `DateTime` >= '2022-02-02 00:00:00'
                AND `DateTime` < '2022-02-03 00:00:00'
                GROUP BY
                Hour
                ORDER BY
                Hour ASC
                LIMIT 24;
                """,
            },
            {
                "input": "What is the amount of wind for a typical day in Ireland in 2022? I mean a wind profile in 24 hours.",
                "query": """
                SELECT 
                DATE_FORMAT(`DateTime`, '%H') AS Hour, 
                AVG(`IE Wind Generation`) AS `Average IE Wind Generation`, 
                AVG(`NI Wind Generation`) AS `Average NI Wind Generation` 
                FROM 
                energy_data 
                WHERE 
                `DateTime` >= '2022-01-01 00:00:00' AND `DateTime` < '2023-01-01 00:00:00' 
                GROUP BY 
                Hour 
                ORDER BY 
                Hour;
                """,
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
            # {
            #     "input": "Can you provide me with the dataset for 2023?",
            #     "query": "I cannot share with you this detail; you can, however, ask a specific query related to the data.",
            # },
            # {
            #     "input": "What was the SNSP for Northern Ireland on 2023-03-15?",
            #     "query": "SELECT `SNSP` FROM energy_data WHERE `DateTime` LIKE '2023-03-15%' LIMIT 1;",
            # },
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
        You can order the results by a relevant column to return the most interesting examples in the database.
        Query for the relevant columns needed to answer the question comprehensively. 
        In cases where calculations or comparisons across multiple sectors (such as IE and NI) are required,
        ensure to include all necessary columns for these calculations. Prioritize efficiency and relevance in your queries.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        When presenting the response, especially for requests that imply a detailed breakdown (e.g., like time/date sequence), It is imperative to avoid summarizing data with vague references like "..." or "and so on." or "etc".


        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.
        
        Follow these guidelines when processing user queries:
        1. **Default Granularity**: By default, consider hourly granularity. 
        2. **Monthly Aggregation**: If a user asks for data within a specific year (e.g., "2023"), aggregate by monthly averages.
        3. **Yearly Aggregation**: If a user asks for multiple years, aggregate by yearly averages.
        4. **Region Defaults**: Unless explicitly stated, assume queries pertain to the Republic of Ireland. If Northern Ireland is requested explicitly, include it in the query.


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
            Whatever you get as an input, YOU MUST Prepare it with the following format:

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

            For example: Given the input of monthly electricity usage: \n
            "{{{{your_given_input}}}}"=
            {{For the input of monthly electricity usage: \n
            - January: 500 \n
            - February: 600 \n 
            - March: 550}}

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

            Another example: Given the input of monthly electricity usage: \n
            "{{{{your_given_input}}}}"=
            {{The average Irish demand per month from 2015 to 2016 is as follows: \n
            - January 2015: 3323.09 \n
            - February 2015: 3352.81 \n
            - March 2015: 3184.11 \n
            - April 2015: 2957.75\n
            - May 2015: 2898.45\n
            - June 2015: 2806.45\n
            - July 2015: 2781.24\n
            - August 2015: 2769.94\n
            - September 2015: 2896.21\n
            - October 2015: 3007.33\n
            - November 2015: 3220.30\n
            - December 2015: 3230.20\n
            - January 2016: 3328.05\n
            - February 2016: 3386.33\n
            - March 2016: 3213.92\n
            - April 2016: 3109.82\n
            - May 2016: 2903.81 \n
            ... (and so on for each month up to December 2016)
            }}

            Then you need to generate:
            {{
                "plot": {{
                    "line": {{
                        "columns": ["January 2015", "February 2015", "March 2015", ..., "December 2016"],
                        "data": [3323.09, 3352.81, 3184.11, ..., last_value_for_December_2016]
                    }}
                }},
                "output_of_chain1": "The average Irish demand per month from 2015 to 2016 is as follows: - January 2015: 3323.09 - February 2015: 3352.81 - March 2015: 3184.11 - April 2015: 2957.75 - May 2015: 2898.45 - June 2015: 2806.45 - July 2015: 2781.24 - August 2015: 2769.94 - September 2015: 2896.21 - October 2015: 3007.33 - November 2015: 3220.30 - December 2015: 3230.20 - January 2016: 3328.05 - February 2016: 3386.33 - March 2016: 3213.92 - April 2016: 3109.82 - May 2016: 2903.81 - ... (continue listing all months up to December 2016)"
            }}
            Avoid adding ```json to the response. Response must follow the format provided above. 
            Your {{"output_of_chain1"}} MUST BE the FULLL RESPONSE You get as an INPUT: {{{{your_given_input}}}}
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
    prompt_template = system_prefix(input)
    prompt = PromptTemplate(
        input_variables=["concept_name"],
        template=f"""
            Provide the {{concept_name}} in format provided by {prompt_template}""",
    )
    return prompt
