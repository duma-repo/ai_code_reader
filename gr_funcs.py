import re
import time

import gradio as gr
import utils
import gpt_server

llm_response = {}


def analyse_project(prj_path, progress=gr.Progress()):
    global llm_response
    llm_response = {}
    file_list = utils.get_all_files_in_folder(prj_path)

    for i, file_name in enumerate(file_list):
        relative_file_name = file_name.replace(prj_path, '.')
        progress(i / len(file_list), desc=f'正在阅读：{relative_file_name}')

        with open(file_name, 'r', encoding='utf-8') as f:
            file_content = f.read()

        sys_prompt = "你是一位资深的程序员，正在帮一位新手程序员阅读某个开源项目，我会把每个文件的内容告诉你，" \
                     "你需要做一个新手程序员阅读的，简单明了的总结。用MarkDown格式返回（必要的话可以用emoji表情增加趣味性）"
        user_prompt = f"源文件路径：{relative_file_name}，源代码：\n```\n{file_content}```"

        response = gpt_server.request_llm(sys_prompt, [(user_prompt, None)])
        llm_response[file_name] = next(response)

    return '阅读完成'


def get_lang_from_file(file_name):
    if file_name.endswith('.py'):
        return 'python'
    elif file_name.endswith('.md'):
        return 'markdown'
    elif file_name.endswith('.json'):
        return 'json'
    elif file_name.endswith('.html'):
        return 'html'
    elif file_name.endswith('.css'):
        return 'css'
    elif file_name.endswith('.yaml'):
        return 'yaml'
    elif file_name.endswith('.sh'):
        return 'shell'
    elif file_name.endswith('.js'):
        return 'javascript'

    return None


def view_prj_file(selected_file):
    global llm_response
    if not llm_response or selected_file not in llm_response:  # 没有gpt的结果，只查看代码
        gpt_res_update = gr.update('gpt_res', visible=False)
        gpt_label_update = gr.update('gpt_label', visible=False)
        gpt_res_text = ''
    else:
        gpt_res_update = gr.update('gpt_res', visible=True)
        gpt_label_update = gr.update('gpt_label', visible=True)
        gpt_res_text = llm_response[selected_file]

    if selected_file.endswith('.py'):
        yield gr.update('code', visible=True, language='python'), gpt_label_update, gpt_res_update
    elif selected_file.endswith('.json'):
        yield gr.update('code', visible=True, language='json'), gpt_label_update, gpt_res_update
    else:
        yield gr.update('code', visible=True, language=None), gpt_label_update, gpt_res_update

    yield (selected_file,), [[None, None]], gpt_res_text


def gen_prj_summary_prompt():
    prefix_prompt = '这里有一个代码项目，里面的每个文件的功能已经被总结过了。' \
                    '你需要根据每个文件的总结内容，做一个整体总结，简单明了，突出重点。' \
                    '用Markdown格式返回，必要时可以使用emoji表情。每个文件路径以及总结如下：\n'

    prompt = prefix_prompt
    for file_path, file_summary in llm_response.items():
        file_prompt = f'文件名：{file_path}\n文件总结：{file_summary} \n\n'
        prompt = f'{prompt}{file_prompt}'

    suffix_prompt = '你做的是类似"README"对整个项目的总结，而不需要再对单个文件做总结。"'
    return f'{prompt}{suffix_prompt}'


def prj_chat(user_in_text: str, prj_chatbot: list):
    sys_prompt = "你是一位资深的导师，指导算法专业的毕业生写论文，这里有些代码需要总结，也有一些论文改写工作需要你指导。"
    prj_chatbot.append([user_in_text, ''])
    yield prj_chatbot

    if user_in_text == '总结整个项目':  # 新起对话，总结项目
        new_prompt = gen_prj_summary_prompt()
        print(new_prompt)
        llm_response = gpt_server.request_llm(sys_prompt, [(new_prompt, None)], stream=True)
    else:
        llm_response = gpt_server.request_llm(sys_prompt, prj_chatbot, stream=True)

    for chunk_content in llm_response:
        prj_chatbot[-1][1] = chunk_content
        yield prj_chatbot


def clear_textbox():
    return ''


def view_uncmt_file(selected_file):
    lang = get_lang_from_file(selected_file)
    return gr.update(language=lang, value=(selected_file,)), gr.update(variant='primary', interactive=True,
                                                                       value='添加注释'), gr.update(visible=False)


def ai_comment(btn_name, selected_file):
    if btn_name != '添加注释':
        yield btn_name, gr.update(visible=False)
    else:
        yield '注释添加中...', gr.update(visible=False)

        lang = get_lang_from_file(selected_file)
        with open(selected_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        sys_prompt = "你是一位资深的程序员，能够读懂任何代码，并为其增加中文注释，如果是函数，需要为函数docstrings格式的注释。" \
                     "直接返回修改的结果，不需要其他额外的解释。"
        user_prompt = f"源代码：\n```{file_content}```"

        response = gpt_server.request_llm(sys_prompt, [(user_prompt, None)])
        res_code = next(response)
        if res_code.startswith('```') and res_code.endswith('```'):
            code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', res_code, re.DOTALL)
            res_code = code_blocks[0]

        yield '添加注释', gr.update(visible=True, language=lang, value=res_code)


def model_change(model_name):
    gpt_server.set_llm(model_name)

    return model_name


def view_raw_lang_code_file(selected_file):
    lang = get_lang_from_file(selected_file)
    return gr.update(language=lang, value=(selected_file,))\
        , gr.update(variant='primary', interactive=True, value='转换')\
        , gr.update(visible=False)


def change_code_lang(btn_name, raw_code, to_lang):
    if btn_name != '转换':
        yield btn_name, gr.update(visible=False)
    else:
        yield '语言转换中...', gr.update(visible=False)

        sys_prompt = f"你是一位资深的程序员，可以一些任何编程语言的代码，我需要你将下面的代码转成`{to_lang}`语言的代码。要求：\n" \
                     f"- 保证转换后的代码是正确的\n" \
                     f"- 对于无法转换的情况，可以不转，但需要进行说明\n" \
                     f"- 如果遇到第三方库，需要说明在目标变成语言中，依赖什么库，如果目标编程语言没有对应的库，也进行说明\n" \
                     f"- 用Markdown格式返回，内容简单明了，不要太啰嗦"
        user_prompt = f"源代码：\n```{raw_code}```"

        response = gpt_server.request_llm(sys_prompt, [(user_prompt, None)])
        res = next(response)

        yield '转换', gr.update(visible=True, value=res)
