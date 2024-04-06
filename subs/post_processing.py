import json


def post_process_chain_response(response_of_chain):
    # Convert the response string into a dictionary
    response_1 = json.dumps(response_of_chain)

    response_2 = json.loads(response_1)

    response_3 = json.loads(response_2)

    # Initialize default values for plot_info and prompt_info in case they are not set
    plot_info = None
    prompt_info = None

    # Check if 'plot' key exists in the response, if so, assign its value to plot_info
    if "plot" in response_3:
        plot_info = response_3["plot"]
    else:
        # Handle the case where 'plot' is not in the response
        # You might want to log an error, set a default value, or take some other action
        print("Warning: 'plot' key not found in response.")

    # Similarly, check if 'output_of_chain1' exists and assign its value to prompt_info
    if "output_of_chain1" in response_3:
        if response_3["output_of_chain1"] == "I do not know.":
            prompt_info = "Sorry, I cannot answer the question. You may want to rephrase your query or provide more precise details."
    else:
        # Handle the case where 'output_of_chain1' is not in the response
        print("Warning: 'output_of_chain1' key not found in response.")

    # Return the gathered information
    return plot_info, prompt_info
