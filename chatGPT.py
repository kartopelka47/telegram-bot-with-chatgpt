import openai

from asyncio.threads import to_thread


class GPT:
    def __init__(self, token, request_text):
        self.received_text = None
        self.token = token
        self.request_text = request_text



    async def standart_request(self):
        """
        :return: receive text from ChatGPT
        """
        openai.api_key = self.token
        MODEL = "gpt-3.5-turbo"
        response = await to_thread(openai.ChatCompletion.create, model=MODEL,
                                   messages=[
                                       {"role": "user", "content": self.request_text}
                                   ],
                                   temperature=0
                                   )
        received_text = response["choices"][0]["message"]["content"]
        self.received_text = received_text
        return received_text

    async def ukrainisation_request(self):
        """
        :return: receive text from ChatGPT
        """
        openai.api_key = self.token
        MODEL = "gpt-3.5-turbo"
        response = await to_thread(openai.ChatCompletion.create, model=MODEL,
                            messages=[
                               {"role": "user", "content": self.request_text},
                               {"role": "system", "content": "You must speak only Ukrainian"}
                           ],
                           temperature=0
                            )
        received_text = response["choices"][0]["message"]["content"]
        self.received_text = received_text
        return received_text

    async def choose_gpt_type(self, gpt_type) -> str:
        """
        :type gpt_type: str
        """
        if gpt_type == "default_gpt":
            text = await self.standart_request()
            return text
        elif gpt_type == "ukrainisation_gpt":
            text = await self.ukrainisation_request()
            return text

    # dict_of_gpt_type = {
    #     "default_gpt": lambda: GPT.standart_request(),
    #     "ukrainisation_gpt": lambda: GPT.ukrainisation_request()
    # }

