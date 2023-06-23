import openai

class GPT:
    def __init__(self, token, request_text):
        self.received_text = None
        self.token = token
        self.request_text = request_text

    async def write_request(self):
        """
        :type token: str
        :type request_text: str
        :return: receive text from ChatGPT
        """
        openai.api_key = self.token
        MODEL = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": self.request_text}
                # {"role": "system", "content": "You should only answer speak in germany"}
            ],
            temperature=0
        )
        received_text = response["choices"][0]["message"]["content"]
        self.received_text = received_text
        return received_text
    
    
    
    # async def write_request(self, token, request_text):
    #     """
    #     :type token: str
    #     :type request_text: str
    #     :return: receive text from ChatGPT
    #     """
    #     openai.api_key = token
    #     MODEL = "gpt-3.5-turbo"
    #     response = openai.ChatCompletion.create(
    #         model=MODEL,
    #         messages=[
    #             {"role": "user", "content": request_text}
    #             # {"role": "system", "content": "You should only answer speak in germany"}
    #         ],
    #         temperature=0
    #     )
    #     received_text = response["choices"][0]["message"]["content"]
    #     return received_text
