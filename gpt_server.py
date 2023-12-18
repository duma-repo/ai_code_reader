from llms.llm import LLM

model: LLM = None


def set_llm(model_name):
    global model

    model_cat = model_name.split('-')[0]
    if model_cat == 'gpt':
        from llms.chatgpt import ChatGPT
        model = ChatGPT(model_name)
    elif model_cat == 'chatglm3':
        from llms.chatglm import ChatGLM3
        model = ChatGLM3(model_name)
    elif model_cat == 'Qwen':
        from llms.qwen import Qwen
        model = Qwen(model_name)
    else:
        raise Exception(f'不支持的模型 {model_name}')


def request_llm(sys_prompt: str, user_prompt: list, stream=False):
    return model.request(sys_prompt, user_prompt, stream)
