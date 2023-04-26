import requests
import json
import argparse
import sys


class Sender:

  def __init__(self, params):

    self.params = params
    self.sender_initializer()

  def sender_initializer(self):

    with open(self.params, "r") as json_file:
      params = json.load(json_file)

    self.channelid = params['channelid']
    self.authorization = params['authorization']
    self.application_id = params['application_id']
    self.guild_id = params['guild_id']
    self.session_id = params['session_id']
    self.version = params['version']
    self.id = params['id']
    self.flags = params['flags']

  def send(self, message_id, number,uuid):
        header = {'authorization': self.authorization}
        payload = {'type': 3,
                   'application_id': self.application_id,
                   'guild_id': self.guild_id,
                   'channel_id': self.channelid,
                   'session_id': self.session_id,
                   "message_flags": 0,
                   "message_id": message_id,
                   "data": {"component_type": 2, "custom_id": f"MJ::JOB::upsample::{number}::{uuid}"}}

        r = requests.post('https://discord.com/api/v9/interactions',
                          json=payload,
                          headers=header)
        while r.status_code != 204:
            r = requests.post('https://discord.com/api/v9/interactions',
                              json=payload,
                              headers=header)

        print('Upscale request for message_id [{}] and number [{}] successfully sent!'.format(message_id, number))

