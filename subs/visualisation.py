import pandas as pd
import streamlit as st


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        # df.set_index("columns", inplace=True)
        # Convert the 'columns' to an ordered Categorical type based on the existing order
        df.set_index(
            pd.CategoricalIndex(df["columns"], categories=df["columns"], ordered=True),
            inplace=True,
        )

        # Display dataframe in a table
        st.dataframe(df)

        df.drop(
            "columns", axis=1, inplace=True
        )  # Remove the columns column if it's no longer needed as a separate column

        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
