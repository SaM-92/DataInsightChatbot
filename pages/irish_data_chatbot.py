from subs.agent import generate_sql_and_plot

import streamlit as st


def irish_data_chatbot():
    # This will create a text area for user input and store it in 'query'
    query = st.text_area(
        "Please ask your question 👇🏻",
        placeholder="Example: What is the average wind generation in Ireland in 2023, averaged by month?",
    ).strip()  # .strip() removes any leading/trailing whitespace

    # Initialize or update the session state for handling button press
    if "button_pressed" not in st.session_state:
        st.session_state["button_pressed"] = False

    # Button to submit the query
    if st.button("Submit"):
        st.session_state["button_pressed"] = True

    # Only process the query after the user presses the 'Submit' button and ensures query is not empty
    if st.session_state["button_pressed"] and query:
        # with st.spinner("Processing your request... Please wait."):
        #     chain_Final = configure_sequential_chain(
        #         chain_id_sql="chain_1", chain_id_response_plot="chain_2"
        #     )

        #     response_of_chain = chain_Final.run(query)

        #     plot_info, prompt_info = post_process_chain_response(response_of_chain)

        #     # Reset button press state after processing
        #     st.session_state["button_pressed"] = False

        with st.spinner("🚀 Processing your request... Please wait ⏳"):
            # Example of using the function
            chain_id_sql = "chain_1"
            chain_id_response_plot = "chain_2"
            # Call the function to generate SQL and plot results
            sql_output, plot_output = generate_sql_and_plot(
                chain_id_sql, chain_id_response_plot, query
            )

            # Reset button press state after processing
            st.session_state["button_pressed"] = False

            # Display responses or errors based on the processing results
            if sql_output:
                st.write(sql_output)
            else:
                st.write(
                    "Sorry, I cannot answer the question. You may want to rephrase your query or provide more precise details."
                )

            if plot_output:
                # write_response(plot_info)
                print(plot_output)
                plot_area = st.empty()
                plot_area.pyplot(exec(plot_output))
            else:
                st.write("Unable to generate plot based on the provided data.")
    else:
        # Optionally, show a message or leave blank if no query has been submitted yet
        st.write("Please enter a query and press submit to see the response.")
