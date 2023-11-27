from openai import OpenAI

# 如果是国内转发的API，则修改 base_url
client = OpenAI(base_url='xxx',
                api_key='sk-xxx')
model_name = 'gpt-3.5-turbo-1106'


def request_llm(sys_prompt: str, user_prompt: list, server_name='openai', stream=False):
    if server_name == 'openai':
        return request_openai(sys_prompt, user_prompt, stream)
    else:
        pass


def get_response(response, stream: bool):
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


def request_openai(sys_prompt, user_prompt: list, stream=False):
    req_msgs = [
        {"role": "system", "content": f"{sys_prompt}"},
    ]
    for prompt in user_prompt:
        req_msgs.append({"role": "user", "content": f"{prompt[0]}"})

        if len(prompt) == 2:
            req_msgs.append({"role": "assistant", "content": f"{prompt[1]}"})
        else:
            break

    response = client.chat.completions.create(
        model=model_name,
        messages=req_msgs,
        stream=stream
    )
    res = get_response(response, stream)

    return res
