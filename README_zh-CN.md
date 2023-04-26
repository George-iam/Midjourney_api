# Midjourney_api
非官方的Midjourney API

这是自定义的Midjourney API。使用它，你可以通过代码生成图片。正在研究Discord API。

!! 不要忘记Modjourney TOS不允许任何自动化，所以这个项目是研究的唯一目的!

包含： 
- 发送器：用于向Midjourney发送提示信息。
- 接收器：在终端工作，将所有完成的图像下载到本地文件夹。
- web_api：提供API服务

安装：
1. 创建Discord账户，并创建你的服务器(指示在这里: https://discord.com/blog/starting-your-first-discord-server)
2. 创建Midjourney账户并邀请Midjourney Bot到你的服务器(说明在这里: https://docs.midjourney.com/docs/invite-the-bot)
3. 确保从你的服务器上生成工作
4. 在Chrome浏览器中登录Discord，打开你的服务器的文本频道，点击右上角的三个点，然后是更多工具，然后是开发工具。
选择网络标签，你会看到你的页面的所有网络活动。
5. 现在在你的输入框中输入任何要生成的提示，在你按下回车键发送带有提示的信息后，你会在网络活动中看到名为 "interaction "的新行。
按下它并选择Payload标签，你会看到payload_json--这就是我们需要的东西！
复制channelid、authorization(在请求标头中）、application_id、guild_id、session_id、version和id值，我们稍后会需要它。
6. clone repo
7. 7.打开 "sender_params.json "文件，把第5段中的所有值都放到里面。同时填写'flags'字段，为你的提示指定特殊标志。
8. 现在你已经准备好运行文件了：
- 要启动接收器脚本，请打开终端并输入：
python /path/to/cloned/dir/receiver.py --params /path/to/cloned/dir/sender_params.json --local_path '/path/to/folder/for/downloading/images' 。
这个脚本将显示所有的生成进度，并在准备好后立即下载图片。
- 为了发送生成的提示，打开另一个终端并输入
python //path/to/cloned/dir/sender.py --params /path/to/cloned/dir/sender_params.json --prompt 'your prompt here
9. 享受吧 :)

注意控制并行请求的数量 - 对于正常和最快的工作，它不应该大于3（在基本和标准计划中，专业计划中为12）。

## （更新）外部API使用介绍：
- 要使用外部API，nano app.py（配置跨域与sender_params.json文件路径)
- python app.py
### 请求方式
- post请求：http://localhost:5000/api/send_and_receive"
- 可选参数：cdn=true(默认false，启用后服务器将缓存图片然后再发送，大陆访问更友好）
例子：
```python
import requests
import json

payload = {
    "prompt"： "your_prompt_here"
}

url = "http://localhost:5000/api/send_and_receive"；

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

print(response.json())
```
- get请求：http://localhost:5000/upscale"
- 必填参数：file_name(string），需要执行upscale的文件名（例如rockgifinrock1971_link_and_zelda_33e8886f-adae-4579-9882-bae644005f5b.png）
- 必填参数：number（number），需要执行upscale的图片序号（例1/2/3/4）。
- 可选参数：cdn=true(默认false，启用后服务器将缓存图片然后再发送，大陆访问更友好）
例子：
```python
import requests

base_url = 'http://localhost:5000'  # 替换为您的 Flask 应用实际运行的 URL
file_name = 'rockgifinrock1971_link_and_zelda_33e8886f-adae-4579-9882-bae644005f5b.png'  # 替换为您的实际文件名
number = 3  # 替换为您想要使用的数字

response = requests.get(f'{base_url}/upscale', params={'file_name': file_name, 'number': number})

if response.status_code == 200:
    print('Success!')
    print(response.json())
else:
    print(f'Error: {response.status_code}')
    print(response.text)
```

### CDN缓存的图片存在同目录文件夹下，可按需清理。数据库每24小时自动刷新，防止过期图片。
- 中文支持可以联系me@hiripple.com

项目评论：

这是第一个简单的API版本，现在我正在开发下一个版本：
- 本地队列控制器
- 能够与任何数量的Midjourney账户并行工作，以获得更好和可扩展的性能。
- 还有很多其他的东西。


联系方式：

如需建议和合作：
normalabnormalai@gmail.com

为了帮助该项目，USDT（ERC20）钱包：0x589c18c17ef4fea0acea476fd4973dc5da82835c


