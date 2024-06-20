from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import os
import streamlit as st


def connect_to_irish_db(cloud=True):
    """Connect to the SQLite database holding Irish power system data.

    Args:
        cloud (bool, optional): True if we are running the code on the cloud. Defaults to True.

    Returns:
        SQLDatabase: An instance of the SQLDatabase class connected to the Irish power system data.
    """

    # Get the DATABASE_URL from environment variable or use the Heroku PostgreSQL URL directly
    if cloud is True:
        DATABASE_URL = os.environ["DATABASE_URL"]

        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

        if not DATABASE_URL:
            raise ValueError("No DATABASE_URL environment variable set")

        # Create an SQLAlchemy engine
        engine = create_engine(DATABASE_URL)

        # Create a LangChain SQLDatabase instance using the SQLAlchemy engine
        db = SQLDatabase(engine)
        print("Successfully connected to the PostgreSQL")
        st.write("🫡 We are fetching data for you!")
        return db

    else:
        db = SQLDatabase.from_uri("sqlite:///./data/eirgrid_data.db")
        return db
