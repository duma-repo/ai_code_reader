
class LLM:
    def __init__(self, model_name):
        self.model_name = model_name

    def request(self, sys_prompt, user_prompt: list, stream=False):
        pass
