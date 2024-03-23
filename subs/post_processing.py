import json


def post_process_chain_response(response_of_chain):

    # Convert the response string into a dictionary
    response_dict = json.loads(response_of_chain)

    # # # Access the 'plot' part of the response
    # plot_info = response_dict["plot"]

    # # # Access the 'prompt' part of the response
    # prompt_info = response_dict["prompt"]

    # return plot_info, prompt_info
    return response_dict
