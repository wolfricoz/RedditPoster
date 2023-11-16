import json
import os


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        if os.path.exists(self.config_file):
            self.config = self.load_config()
            self.config = self.update_config()
            return
        self.create_config()
        self.config = self.load_config()

    def get_key(self, key: str):
        """Returns a key from the config file"""
        return self.config.get(key, "")

    def create_config(self):
        """Creates a config file with default values"""
        config_file_split = self.config_file.split("/")
        if len(config_file_split) > 1 and os.path.exists(config_file_split[0]) is False:
            os.mkdir(config_file_split[0])

        config = {
            "subreddits": [],
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def update_config(self):
        """Updates the config file with the current values"""
        config = {
            "subreddits"   : self.config.get("subreddits", []),
            "title"        : self.config.get("title", ""),
            "body"         : self.config.get("body", ""),
            "client_id"    : self.config.get("client_id", ""),
            "client_secret": self.config.get("client_secret", ""),
            "user_agent"   : self.config.get("user_agent", ""),
            "redirect_uri" : self.config.get("redirect_uri", "http://localhost:8080"),
            "refresh_token": self.config.get("refresh_token", "")
        }
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        return config

    def load_config(self):
        """Loads the config file"""
        with open(self.config_file) as f:
            config = json.load(f)
        return config

    def add_subreddit(self, subreddit: str):
        """Adds a subreddit to the config file"""
        self.config["subreddits"].append(subreddit)
        self.update_config()

    def save_string(self, key, string: str):
        """Saves a string to the config file"""
        self.config[key] = string
        self.update_config()

    def remove_subreddit(self, subreddit: str):
        """Removes a subreddit from the config file"""
        self.config["subreddits"].remove(subreddit)
        self.update_config()

    def get_subreddits(self):
        """Returns a list of subreddits"""
        subreddits: list = self.config.get("subreddits", [])
        subreddits.sort()
        return subreddits

    def get_config(self):
        """Returns the config"""
        return self.config
