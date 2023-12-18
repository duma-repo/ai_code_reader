# 项目
[prj]
# 【必须设置】待分析项目的绝对路径
dir=

# 配置 openai 相关的参数
[openai]
# 【非必须设置】chatgpt的接口url，如果使用的是非官网，如：国内转发的接口，则需要修改为你的url
base_url=https://api.openai.com/v1
# 【非必须设置】配置代理，若使用官网接口，并且是国内网络环境，则需要设置代理。
http_proxy=
https_proxy=
# 【非必须设置】如果使用chatgpt分析必须设置，若使用开源大模型，不必设置
api_key=sk-

# 配置本地大模型相关的参数
[local_llm]
# 【非必须设置】如果使用开源大模型，需要设置本地大模型缓存的绝对路径
modelscope_cache=