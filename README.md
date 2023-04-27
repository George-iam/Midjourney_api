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


Project comments:

This is the first simple API version, now I'm working on next one with:
- local queue controller
- ability to work with any number of Midjourney accounts in parralel to get much better and scalable performance
- Upsampling script to send upsample request
- And lots of other things.


Contacts:

For proposals and cooperation:

email: normalabnormalai@gmail.com

WeChat ID: george-iam

Discord: georgeb#0907
