import openai

from asyncio.threads import to_thread


class GPT:
    def __init__(self, token, request_text):
        self.received_text = None
        self.token = token
        self.request_text = request_text

    async def standart_request(self):
        """
        :type token: str
        :type request_text: str
        :return: receive text from ChatGPT
        """
        openai.api_key = self.token
        MODEL = "gpt-3.5-turbo"
        response = await to_thread(openai.ChatCompletion.create, model=MODEL,
                                   messages=[
                                       {"role": "user", "content": self.request_text}
                                       # {"role": "system", "content": "You must speak only Ukrainian"}
                                   ],
                                   temperature=0
                                   )
        # return "ти шо даун?"
        received_text = response["choices"][0]["message"]["content"]
        self.received_text = received_text
        return received_text
