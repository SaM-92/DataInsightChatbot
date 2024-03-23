from langchain_community.utilities import SQLDatabase


def connetc_to_irish_db():
    """Connect to the SQLite database holding Irish power system data.

    Returns:
        SQLDatabase: An instance of the SQLDatabase class connected to the Irish power system data.
    """
    # import os

    # print("Current Working Directory:", os.getcwd())

    db = SQLDatabase.from_uri("sqlite:///./data/eirgrid_data.db")
    return db
