import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from subs.agent import configure_sequential_chain
from subs.post_processing import post_process_chain_response

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


# Check current working directory.
print("Current Working Directory: ", os.getcwd())


st.title("👨‍💻 Chat with Irish Power System Data")

st.write("Please ask your question.")

# # data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")


chain_Final = configure_sequential_chain(
    chain_id_sql="chain_1", chain_id_response_plot="chain_2"
)

if query:
    response_of_chain = chain_Final.run(query)

    # from subs.post_processing import post_process_chain_response

    # plot_info, prompt_info = post_process_chain_response(response_of_chain)
    # print("infooo", plot_info)
    # print("info2", prompt_info)

    response_for = post_process_chain_response(response_of_chain)

    st.write(response_for["output_of_chain1"])
    from subs.visualisation import write_response

    write_response(response_for)
