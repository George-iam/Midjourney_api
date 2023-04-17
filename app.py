import time
from flask import Flask, request, jsonify
from sender import Sender
from url_receiver import Receiver

# 创建 Flask 应用
app = Flask(__name__)

request_in_progress = False

# 创建一个 API 路由，接受 POST 请求，用户通过关键词参数发送请求
@app.route('/api/send_and_receive', methods=['POST'])
def send_and_receive():
    global request_in_progress

    if request_in_progress:
        return jsonify({'error': 'The current queue is full, please try again later（当前队列已满，请稍后再试）'})

    request_in_progress = True

    # 从请求中获取关键词参数
    data = request.get_json()
    prompt = data.get('prompt')
    sender = Sender(params)
    sender.send(prompt)

    # 使用 Receiver 类接收图片 URL
    receiver = Receiver(params)
    receiver.collecting_results()

    # 记录当前已检测到的图片数量
    initial_image_count = len(receiver.df.index)

    # 等待新图片出现
    max_wait_time = 600  # 最大等待时间，单位为秒
    wait_time = 0
    while wait_time < max_wait_time:
        receiver.collecting_results()
        current_image_count = len(receiver.df.index)

        if current_image_count > initial_image_count:
            # 发现新图片，跳出循环
            break

        # 等待一段时间
        time.sleep(1)
        wait_time += 1

    if current_image_count > initial_image_count:
        latest_image_id = receiver.df.index[-1]
        latest_image_url = receiver.df.loc[latest_image_id].url
    else:
        latest_image_url = None

    request_in_progress = False

    # 将最新图片的URL作为响应返回
    return jsonify({'latest_image_url': latest_image_url})

if __name__ == "__main__":

    # 指定参数，这里修改为您提供的路径
    params = '/root/Midjourney_api/sender_params.json'

    # 启动 Flask 应用
    app.run(debug=True, host='0.0.0.0')
