import os
import json
from pathlib import Path


class Config:

    def __init__(self):
        self.config_dir = Path.home() / ".plexcontentmanager"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self):
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)

        if not self.config_file.exists():
            default_config = {
                "server_url": "",
                "token": "",
                "libraries": []
            }
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=4)
            return default_config

        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {
                "server_url": "",
                "token": "",
                "libraries": []
            }

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_server_url(self):
        return self.config.get("server_url", "")

    def get_token(self):
        return self.config.get("token", "")

    def set_server_url(self, url):
        self.config["server_url"] = url
        self.save_config()

    def set_token(self, token):
        self.config["token"] = token
        self.save_config()
