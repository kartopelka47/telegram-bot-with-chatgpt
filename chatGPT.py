import openai

def write_request(token,request_text):
    """
    :type token: str
    :type request_text: str
    :return: receive text from ChatGPT
    """
    openai.api_key = token
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": request_text}
            # {"role": "system", "content": "You should only answer speak in germany"}
        ],
        temperature=0,
    )

    # response = openai.ChatCompletion.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "user", "content": request_text},
    #         {"role": "assistant", "content": "bobr"}
    #     ],
    #     temperature=0,
    # )
    received_text = response["choices"][0]["message"]["content"]
    return received_text