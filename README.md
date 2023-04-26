[中文版本](https://github.com/CelestialRipple/Midjourney_api/blob/main/README_zh-CN.md)
# Midjourney_api
unofficial Midjourney API

This is custom Midjourney API. Using it you could generate images by code. Working on Discord API.

!! Don't forget Modjourney TOS doesn't allow any automation, so this project is research only purpose !!

Contains: 
- Sender: for sending prompts to Midjourney
- Receiver: works in terminal, download all the completed images to local folder

Installation:
1. Create Discord account and create your server(instruction here: https://discord.com/blog/starting-your-first-discord-server)
2. Create Midjourney account and invite Midjourney Bot to your server (instruction here: https://docs.midjourney.com/docs/invite-the-bot)
3. Make sure generation works from your server
4. Log in to Discord in Chrome browser, open your server's text channel, click on three points upper right corner, then More Tools and then Developer Tools.
Select Network tab, you'll see all the network activity of your page.
5. Now type any prompt to generate in your text channel, and after you press Enter to send message with prompt, you'll see in Network Activity new line named "interaction".
Press on it and choose Payload tab and you'll see payload_json - that's what we need!
Copy channelid, authorization, application_id, guild_id, session_id, version and id values, we'll need it a little bit later.
6. Clone this repo
7. Open "sender_params.json" file and put all the values from paragraph 5 to it. Also fill in 'flags' field to specify special flags to your prompts
8. Now you are ready to run files:
- To start receiver script open terminal and type:
python /path/to/cloned/dir/receiver.py --params /path/to/cloned/dir/sender_params.json --local_path '/path/to/folder/for/downloading/images'
This script will show you all the generating progress and download images as soon as it will be ready
- To send prompts for generation open another terminal and type:
python //path/to/cloned/dir/sender.py --params /path/to/cloned/dir/sender_params.json --prompt 'your prompt here'

9. Enjoy :)

Take care of controling number of parralel requests - for normal and fastest work it should be not bigger than 3(in Basic and Standard plan, and 12 in Pro plan).

## (Updated) Introduction to the use of external APIs:
- To use the external API, nano app.py (configure cross-domain with sender_params.json file path)
- python app.py
### Request method
- post request: http://localhost:5000/api/send_and_receive"
- Optional parameter: cdn=true (default false, when enabled the server will cache the image before sending, chinese access is more friendly)
Example:
```python
import requests
import json

payload = {
    "prompt": "your_prompt_here"
}

url = "http://localhost:5000/api/send_and_receive";

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

print(response.json())
```
- get request: http://localhost:5000/upscale"
- Mandatory parameter: file_name(string), the name of the file that needs to be executed upscale (e.g. rockgifinrock1971_link_and_zelda_33e8886f-adae-4579-9882-bae644005f5b.png)
- Mandatory parameter: number (number), the serial number of the image that needs to be executed upscale (example 1/2/3/4).
- Optional parameters: cdn=true (default false, after enabling the server will cache pictures before sending, continental access more friendly)
Example:
```python
import requests

base_url = 'http://localhost:5000' # Replace with the URL your Flask application is actually running on
file_name = 'rockgifinrock1971_link_and_zelda_33e8886f-adae-4579-9882-bae644005f5b.png' # Replace with your actual file name
number = 3 # Replace with the number you want to use

response = requests.get(f'{base_url}/upscale', params={'file_name': file_name, 'number': number})

if response.status_code == 200.
    print('Success!')
    print(response.json())
else.
    print(f'Error: {response.status_code}')
    print(response.text)
```

### CDN cached images exist in the same directory folder and can be cleaned up on demand. The database is automatically refreshed every 24 hours to prevent expired images.
- 中文支持可以联系me@hiripple.com

Translated with www.DeepL.com/Translator (free version)

Project comments:

This is the first simple API version, now I'm working on next one with:
- local queue controller
- ability to work with any number of Midjourney accounts in parralel to get much better and scalable performance
- Upsampling script to send upsample request
- And lots of other things.


Contacts:

For proposals and cooperation:
normalabnormalai@gmail.com

To help the project, USDT (ERC20) wallet: 0x589c18c17ef4fea0acea476fd4973dc5da82835c
