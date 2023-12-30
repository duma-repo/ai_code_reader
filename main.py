import os
import time

import gradio as gr

import config
import gr_funcs
import utils


def main(prj_dir):
    css = """
    #prg_chatbot { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
    #prg_tb { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
    #paper_file { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
    #paper_cb { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
    #paper_tb { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }
    #box_shad { box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.6); /* 设置阴影 */ }

    .markdown-class {
        max-height: 800px;
        overflow-y: scroll;
    }
    """
    with gr.Blocks(title="程序员好基友", theme=gr.themes.Soft(), analytics_enabled=False, css=css) as demo:
        prj_name_tb = gr.Textbox(value=f'{prj_dir}', visible=False)  # 没有实际含义
        with gr.Accordion(label='选择模型（选择开源大模型，如果本地没有，会自动下载，下载完毕后再使用下面的功能）'):
            model_selector = gr.Dropdown(choices=config.model_list, container=False, elem_id='box_shad')
        with gr.Row():
            prj_fe = gr.FileExplorer(label='项目文件', root=prj_dir, file_count='single', scale=1)

        with gr.Accordion(label='chat-code', open=True):
            prj_name = utils.get_prj_name(prj_dir)
            is_embedding = utils.dir_exists(config.PRJ_VECTOR_DB, prj_name)

            with gr.Row():
                if is_embedding:
                    chat_code_reload_btn = gr.Button('加载上次结果', variant='primary')

                chat_code_load_btn = gr.Button('加载项目源码', variant='primary' if not is_embedding else 'secondary')

            # chat_code_label = gr.Label(label="embedding进度", value='等待加载...', visible=False)
            chat_code_label = gr.Text(label="完成项目embedding", visible=False)
            chat_code_cb = gr.Chatbot(label='Chat-Code', elem_id='box_shad')
            with gr.Row():
                chat_code_cb_input = gr.Text(container=False, scale=3, elem_id='box_shad')
                chat_code_cb_send_btn = gr.Button('发送', scale=1, variant='primary')

        with gr.Accordion('阅读项目', open=False):
            with gr.Row():
                code = gr.Code(label='代码', visible=False, elem_id='code', scale=2)
                with gr.Column():
                    gpt_label = gr.Chatbot(label='项目阅读助手', height=40, visible=False, elem_id='gpt_label')  # 没有实际含义
                    gpt_md = gr.Markdown(visible=False, elem_id='llm_res', elem_classes='markdown-class')

            with gr.Row():
                dir_submit_btn = gr.Button('阅读项目', variant='primary')

            with gr.Row():
                label = gr.Label(label="源码阅读进度", value='等待开始...')

        with gr.Accordion(label='对话模式', open=False):
            with gr.Tab('论文改写助手'):
                with gr.Row():
                    prj_chatbot = gr.Chatbot(label='gpt', elem_id='prg_chatbot')
                with gr.Row():
                    prj_chat_txt = gr.Textbox(label='输入框',
                                              value='总结整个项目',
                                              placeholder='请输入...',
                                              container=False,
                                              interactive=True,
                                              scale=5,
                                              elem_id='prg_tb')
                    prj_chat_btn = gr.Button(value='发送', variant='primary', scale=1, min_width=100)
            with gr.Tab('论文阅读助手'):
                with gr.Row():
                    reader_paper = gr.File(scale=1, elem_id='paper_file')
                    with gr.Column(scale=2):
                        with gr.Row():
                            gr.Chatbot(label='论文阅读', scale=2, elem_id='paper_cb')
                        with gr.Row():
                            gr.Text(container=False, scale=2, elem_id='paper_tb', placeholder='请输入...',)
                            gr.Button('发送', min_width=50, scale=1, variant='primary')



        with gr.Accordion(label='代码注释', open=False, elem_id='code_cmt'):
            code_cmt_btn = gr.Button('选择一个源文件', variant='secondary', interactive=False)
            with gr.Row():
                uncmt_code = gr.Code(label='原代码', elem_id='uncmt_code')
                cmt_code = gr.Code(label='注释后代码', elem_id='cmt_code', visible=False)

        with gr.Accordion(label='语言转换', open=False, elem_id='code_lang_change'):
            with gr.Row():
                lang_to_change = [
                    'java', 'python', 'javascript', 'c++', 'php', 'go', 'r', 'perl', 'swift', 'ruby'
                ]
                to_lang = gr.Dropdown(choices=lang_to_change, container=False, value=lang_to_change[0], elem_id='box_shad', interactive=True, scale=2)
                code_lang_ch_btn = gr.Button('选择一个源文件', variant='secondary', interactive=False, scale=1)
            with gr.Row():
                raw_lang_code = gr.Code(label='原代码', elem_id='uncmt_code')
                code_lang_changed_md = gr.Markdown(label='转换代码语言', visible=False, elem_id='box_shad')
                # lang_changed_code = gr.Code(label='抓换后代码', elem_id='cmt_code', visible=False)

        # 模型选择
        model_selector.select(gr_funcs.model_change, inputs=[model_selector], outputs=[model_selector])

        # 监听阅读按钮
        dir_submit_btn.click(gr_funcs.analyse_project, inputs=[prj_name_tb], outputs=[label])
        # 监听文件点击按钮
        prj_fe.change(gr_funcs.view_prj_file, inputs=[prj_fe], outputs=[code, gpt_label, gpt_md])

        # 监听 prj_chat_btn 按钮
        prj_chat_btn.click(gr_funcs.prj_chat, inputs=[prj_chat_txt, prj_chatbot], outputs=[prj_chatbot])
        prj_chat_btn.click(gr_funcs.clear_textbox, outputs=prj_chat_txt)

        # 代码注释模式
        prj_fe.change(gr_funcs.view_uncmt_file, inputs=[prj_fe], outputs=[uncmt_code, code_cmt_btn, cmt_code])
        code_cmt_btn.click(gr_funcs.ai_comment, inputs=[code_cmt_btn, prj_fe], outputs=[code_cmt_btn, cmt_code])

        # 语言转换模式
        prj_fe.change(gr_funcs.view_raw_lang_code_file,
                      inputs=[prj_fe],
                      outputs=[raw_lang_code, code_lang_ch_btn, code_lang_changed_md])
        code_lang_ch_btn.click(gr_funcs.change_code_lang,
                               inputs=[code_lang_ch_btn, raw_lang_code, to_lang],
                               outputs=[code_lang_ch_btn, code_lang_changed_md])

        # chat code
        chat_code_load_btn.click(lambda: gr.update(visible=True), outputs=[chat_code_label])
        chat_code_load_btn.click(gr_funcs.prj_embedding, inputs=[prj_name_tb], outputs=[chat_code_label])

        chat_code_cb_send_btn.click(lambda: '', outputs=[chat_code_cb_input])
        chat_code_cb_send_btn.click(gr_funcs.chat_code_chat, inputs=[chat_code_cb_input, chat_code_cb], outputs=[chat_code_cb])

        if is_embedding:
            chat_code_reload_btn.click(lambda: gr.update(visible=True), outputs=[chat_code_label])
            chat_code_reload_btn.click(gr_funcs.reload_prg_embedding, inputs=[prj_name_tb], outputs=[chat_code_label])

    demo.launch(share=False)


if __name__ == '__main__':
    config.init_config()
    main(os.environ['PRJ_DIR'])
