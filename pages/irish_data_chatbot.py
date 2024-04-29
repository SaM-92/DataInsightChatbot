from subs.agent import configure_sequential_chain
from subs.post_processing import post_process_chain_response
from subs.visualisation import write_response
import streamlit as st


def irish_data_chatbot():
    query = st.text_area("Please ask your question 👇🏻")

    chain_Final = configure_sequential_chain(
        chain_id_sql="chain_1", chain_id_response_plot="chain_2"
    )

    response_of_chain = chain_Final.run(query)

    plot_info, prompt_info = post_process_chain_response(response_of_chain)
    # Check if prompt_info has a meaningful response
    if prompt_info:
        print(prompt_info)
        st.write(prompt_info)
    else:
        # Provide a default response if prompt_info is empty or None
        st.write(
            "Sorry, I cannot answer the question. You may want to rephrase your query or provide more precise details."
        )

    # Only attempt to display the plot if plot_info contains data
    if plot_info:
        write_response(plot_info)
    else:
        # Optionally, handle the case where there's no plot data more explicitly
        # This might be redundant if the message above is sufficient
        st.write("Unable to generate plot based on the provided data.")
