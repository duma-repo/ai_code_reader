from llms.llm import LLM
from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig


class Qwen(LLM):
    def __init__(self, model_name):
        super().__init__(model_name)

        self.tokenizer = AutoTokenizer.from_pretrained(f'qwen/{model_name}', trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(f'qwen/{model_name}', device_map="auto", trust_remote_code=True).eval()

    def request(self, sys_prompt, user_prompt: list, stream=False):
        query, _ = user_prompt[-1]
        query = f'{sys_prompt}\n\n{query}'
        history = []
        for user_content, assistant_content in user_prompt[:-1]:
            history.append({'role': 'user', 'content': user_content})
            history.append({'role': 'assistant', 'content': assistant_content})

        if stream:
            response = self.model.chat_stream(self.tokenizer, query, history=history)
            for chunk in response:
                yield chunk
        else:
            response, _ = self.model.chat(self.tokenizer, query, history=history)
            yield response