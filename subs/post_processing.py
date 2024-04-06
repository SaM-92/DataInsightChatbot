import json


def post_process_chain_response(response_of_chain):

    response_1 = json.dumps(response_of_chain)

    response_22 = json.loads(response_1)

    response_3 = json.loads(response_22)

    # Convert the response string into a dictionary
    # response_dict = json.loads(response_of_chain)

    # # # Access the 'plot' part of the response
    plot_info = response_3["plot"]

    # # Access the 'prompt' part of the response
    prompt_info = response_3["output_of_chain1"]

    return plot_info, prompt_info
    # return response_dict
