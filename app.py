import time
import os
import requests
import re
import threading
import sqlite3
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask import send_from_directory
from sender import Sender
from url_receiver import Receiver
from flask_cors import CORS
from upsender import Sender as UpSender

app = Flask(__name__)
CORS(app, origins="https://example.com")  # 添加 origins 参数以限制允许的来源

request_in_progress = False

def init_db():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (message_id TEXT PRIMARY KEY, url TEXT, filename TEXT)''')
    conn.commit()
    conn.close()
  
def clear_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM images")
    conn.commit()
    conn.close()
  
# 24小时刷新数据库
def clear_database_every_24_hours(db_path):
    while True:
        time.sleep(24 * 60 * 60)  # 等待24小时（24小时 * 60分钟 * 60秒）
        clear_database(db_path)
      
def extract_uuid(filename):
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    match = re.search(uuid_pattern, filename)
    if match:
        return match.group(0)
    else:
        return None
      
def print_stored_data():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    rows = c.fetchall()
    conn.close()

    print("Stored data in the database:")
    print("message_id | url | filename")
    print("---------------------------------------------")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")

def get_message_id_from_db(filename, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询数据库以获取与 filename 相关联的 message_id
    cursor.execute("SELECT message_id FROM images WHERE filename=?", (filename,))
    result = cursor.fetchone()

    if result:
        message_id = result[0]
    else:
        message_id = None

    conn.close()
    return message_id

def reset_request_in_progress():
    global request_in_progress
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

    # 设置最大等待时间
    max_wait_time = 300  # 最大等待时间，单位为秒

    # 创建一个定时器，在最大等待时间后重置request_in_progress标志
    timeout_timer = threading.Timer(max_wait_time, reset_request_in_progress)
    timeout_timer.start()

    # 等待新图片出现
    wait_time = 0
    while wait_time < max_wait_time:
        receiver.collecting_results()
        current_image_count = len(receiver.df.index)

        if current_image_count > initial_image_count:
            # 发现新图片，跳出循环
            timeout_timer.cancel()  # 取消定时器
            break

        # 等待一段时间
        time.sleep(1)
        wait_time += 1

    if current_image_count > initial_image_count:
        latest_image_id = receiver.df.index[-1]
        latest_image_url = receiver.df.loc[latest_image_id].url
        latest_filename = receiver.df.loc[latest_image_id].filename
        cdn = request.args.get('cdn', False)
        if cdn:
            image_filename = download_image(latest_image_url)
            latest_image_url = f"/images/{image_filename}"
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO images (message_id, url, filename) VALUES (?, ?, ?)",
                  (latest_image_id, latest_image_url, latest_filename))
        conn.commit()
        conn.close()

        # 输出存储在数据库中的数据
        print_stored_data()
    else:
        latest_image_url = None
    request_in_progress = False

    # 将最新图片的URL作为响应返回
    return jsonify({'latest_image_url': latest_image_url})
def download_image(url):
    response = requests.get(url)
    filename = secure_filename(os.path.basename(urlparse(url).path))
    image_path = os.path.join('images', filename)
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return filename

@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('images', filename)
                        
@app.route('/upscale', methods=['GET'])
def upscale():
    file_name = request.args.get('file_name')
    number = request.args.get('number')

    if file_name is None or number is None:
        return jsonify({'error': 'Both file_name and number parameters are required'})

    message_id = get_message_id_from_db(file_name, 'images.db')

    if message_id is None:
        return jsonify({'error': f'No message_id found for file_name: {file_name}'})
    sender = UpSender(params)
    uuid = extract_uuid(file_name)
    sender.send(message_id, number, uuid)

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
        cdn = request.args.get('cdn', False)
        if cdn:
            image_filename = download_image(latest_image_url)
            latest_image_url = f"/images/{image_filename}"
        latest_filename = receiver.df.loc[latest_image_id].filename

        # 将 message_id、URL 和文件名存储到数据库
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO images (message_id, url, filename) VALUES (?, ?, ?)",
                  (latest_image_id, latest_image_url, latest_filename))
        conn.commit()
        conn.close()

        # 输出存储在数据库中的数据
        print_stored_data()
    else:
        latest_image_url = None

    request_in_progress = False

    # 将最新图片的URL作为响应返回
    return jsonify({'latest_image_url': latest_image_url})


if __name__ == "__main__":

    # 指定参数，这里修改为您提供的路径
    params = '/home/runner/API-test/sender_params.json'
    init_db();

    db_path = 'images.db'
    clear_db_thread = threading.Thread(target=clear_database_every_24_hours, args=(db_path,))
    clear_db_thread.daemon = True  # 设置为守护线程，这样在主程序结束时，线程也会结束
    clear_db_thread.start()
    app.run(debug=True, host='0.0.0.0')
