import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from subs.agent import configure_sequential_chain
from subs.post_processing import post_process_chain_response
from subs.visualisation import write_response

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


# Check current working directory.
print("Current Working Directory: ", os.getcwd())

st.set_page_config(
    page_title="Emerald Insights",
    page_icon="🏭",
)
st.image("./images/header.png")
st.markdown("Created by Saeed Misaghian")
st.markdown("📧 Contact me: [sam.misaqian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")


st.title("The Irish Power Data Chatbot")
st.markdown(" Evolving Energies: Ten Years of Irish Power Data Unveiled (2014-2024)")

query = st.text_area("Please ask your question 👇🏻")


chain_Final = configure_sequential_chain(
    chain_id_sql="chain_1", chain_id_response_plot="chain_2"
)

if query:
    response_of_chain = chain_Final.run(query)

    plot_info, prompt_info = post_process_chain_response(response_of_chain)
    print(prompt_info)
    st.write(prompt_info)

    write_response(plot_info)
