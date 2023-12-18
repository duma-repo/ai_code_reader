from openai import OpenAI

from llms.llm import LLM


class ChatGPT(LLM):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.client = OpenAI()

    def get_response(self, response, stream: bool):
        if stream:
            return response
            # collected_chunks = []
            # collected_messages = []
            #
            # for chunk in response:
            #     collected_chunks.append(chunk)
            #     chunk_message = chunk.choices[0].delta
            #     if chunk_message.content is not None:
            #         collected_messages.append(chunk_message)
            #
            # return ''.join(collected_messages)
        else:
            return response.choices[0].message.content

    def request(self, sys_prompt, user_prompt: list, stream=False):
        req_msgs = [
            {"role": "system", "content": f"{sys_prompt}"},
        ]
        for prompt in user_prompt:
            req_msgs.append({"role": "user", "content": f"{prompt[0]}"})

            if len(prompt) == 2:
                req_msgs.append({"role": "assistant", "content": f"{prompt[1]}"})
            else:
                break

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=req_msgs,
            stream=stream
        )

        if stream:
            res = ''
            for chunk in response:
                chunk_message = chunk.choices[0].delta
                if chunk_message.content is not None and chunk_message.content != '':
                    res = f'{res}{chunk_message.content}'
                    yield res

        else:
            yield response.choices[0].message.content