from modelscope import snapshot_download, AutoTokenizer, AutoModel

from llms.llm import LLM


class ChatGLM3(LLM):

    def __init__(self, model_name):
        super().__init__(model_name)

        model_dir = snapshot_download("ZhipuAI/chatglm3-6b", revision="v1.0.0")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()

    def request(self, sys_prompt, user_prompt: list, stream=False):
        query, _ = user_prompt[-1]
        query = f'{sys_prompt}\n\n{query}'
        history = []
        for user_content, assistant_content in user_prompt[:-1]:
            history.append({'role': 'user', 'content': user_content})
            history.append({'role': 'assistant', 'content': assistant_content})

        if stream:
            response = self.model.stream_chat(self.tokenizer, query, history=history)
            for chunk in response:
                yield chunk[0]
        else:
            response, _ = self.model.chat(self.tokenizer, query, history=history)
            yield response