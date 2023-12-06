# 项目阅读助手

欢迎大家关注我的公众号**渡码**，大家使用过程中遇到问题，可以在公众号向我提问。AI相关项目、优秀资料都会在公众号首发。


<img  src="./docs/images/screen1.png">

这是运行本地大模型的分支代码，请详细看文档。

### 安装依赖

- python 3.10
- openai                    1.3.3
- gradio                    4.4.1

尤其是python和gradio的版本必须装对，不然无法成功运行。

### 本地大模型配置

1. 目前代码里只支持 chatglm3-6b（其他大模型同理，大家可以自己集成）
   
2. 修改 `gpt_server.py` 文件，第62行，大模型的存储目录（空间要充足）

```python
os.environ['MODELSCOPE_CACHE'] = '模型下载路径'
```

3. 需要调用大模型的地方，修改代码
```python
gpt_server.request_llm(sys_prompt, [(user_prompt, None)])
```
改为
```python
gpt_server.request_llm(sys_prompt, [(user_prompt, None)], 'chatglm3-6b')
```

### 运行

1. 修改 gpt_server.py

```python
client = OpenAI(base_url='xxx', api_key='sk-xxx')
model_name = 'gpt-3.5-turbo-1106'
```

- 首先设置你的api_key
- 如果你用的是官方api_key，可以去掉`base_url`参数，如果是国内访问，自己设置代理
- 如果你用的是国内转发的api_key，`base_url`设置为国内接口地址

2. 打开 main.py，修改项目路径

```python
prj_dir = '项目绝对路径'
```

3. 运行 main.py

```shell
python main.py
```

### 注意事项

1. 关于模型选择，3.5和4.0都可以，我在视频演示用的是3.5(gpt-3.5-turbo-1106)
2. 模型上下文最好在 16k 以上，因为有些源文件比较大，上下文太小可能长度不够
3. 把非源代码的文件删掉，如：压缩文件、图片、模型权重等。阅读这些文件无意义，可能产生不必要的报错，甚至浪费你的api额度
4. **关注你的api额度**，一上来尽量不要读文件多、文件大的项目，建议先用小项目试试，关注一下api额度消耗情况。

这个小项目还有很多不完善的地方，欢迎大家提出改进意见，也欢迎大家提交代码

Bilibili：https://space.bilibili.com/494605864

微信公众号：[渡码](http://mp.weixin.qq.com/profile?src=3&timestamp=1663979948&ver=1&signature=wcyNF3yu1W0bMvEanLaDxbZWIzr4fHOGzS3*iP9FBJmGgREoKU6rifDbYefvfJNkEK2r*hS6httmcHBrvtFoVg==)



<img width="240" src="./docs/images/duma.jpg">
