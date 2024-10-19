from threading import Thread
from requests import Session
import random
import time
import json

class token:
    def __init__(self, token):
        self.token = token
        self.session = Session()
        self.session.headers = {"authorization": self.token, "content-type": "application/json"}
        self.api = "https://discord.com/api"
        self.username = None
        self.id = None
        self.email = None
        self.phone = None

        self._check()

    def _check(self):
        url = self.api + "/users/@me"
        r = self.session.get(url)

        if r.status_code == 200:
            data = r.json()
            self.username = data['username']
            self.id = data['id']
            self.email = data['email']
            self.phone = data['phone']
            return True
        else:
            return False
            exit()

    def send_message(self, msg, channel_id):
        url = self.api + f"/channels/{channel_id}/messages"
        data = {"content": msg}
        r = self.session.post(url, json=data)
        if r.status_code == 200:
            print(f"{self.username} | Message sent to {channel_id}")
            return r.json()["id"]
        else:
            print(f"{self.username} | Error {r.status_code}: {channel_id}")
    def clear_messages(self, channel_id,msgid):
        url = self.api + f"/channels/{channel_id}/messages/{msgid}"
        r = self.session.delete(url)
        print(r.status_code, r.text)

    def dump_info(self, extra_info: bool = False):
        info = {
            "token": self.token,
            "username": self.username,
            "id": self.id,
            "email": self.email,
            "phone": self.phone
        }

        if extra_info:
            info["friends"] = self.get_friends(),
            info["user_dm"] = self.get_user_channels(),
            info["guilds"] = self.get_guilds()

        with open(f"{self.username}.json", "w") as f:
            json.dump(info, f, indent=4)
        print("Info dumped")
    def auto_grind(self, channel_id):
        while True:
            m =self.send_message(1, channel_id)
            self.clear_messages(channel_id,m)
            



