import configparser
import os

model_list = [
    'gpt-3.5-turbo-1106',
    'gpt-4-1106-preview',
    'chatglm3-6b',
    'Qwen-7B-Chat',
    'Qwen-14B-Chat',
    'Qwen-14B-Chat-Int8',
    'Qwen-14B-Chat-Int4'
]


def init_config():
    # 创建一个配置解析器对象
    config = configparser.ConfigParser()
    config.read('.env')

    # 项目目录
    os.environ['PRJ_DIR'] = config.get('prj', 'dir')
    if not os.environ['PRJ_DIR']:
        raise ValueError('没有设置项目路径')

    # 配置 openai 环境变量
    os.environ['OPENAI_BASE_URL'] = config.get('openai', 'base_url')
    os.environ['OPENAI_API_KEY'] = config.get('openai', 'api_key')

    # 设置代理
    http_proxy = config.get('openai', 'http_proxy')
    https_proxy = config.get('openai', 'https_proxy')
    if http_proxy:
        os.environ['http_proxy'] = http_proxy
    if https_proxy:
        os.environ['https_proxy'] = https_proxy

    # 配置本地大模型，魔搭环境变量
    modelscope_cache = config.get('local_llm', 'modelscope_cache')
    if modelscope_cache:
        os.environ['MODELSCOPE_CACHE'] = modelscope_cache
