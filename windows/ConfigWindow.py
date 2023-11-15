"""This window is used to configure the application"""
import tkinter as tk

import classes.config
from classes.reddit import Reddit


class ConfigWindow(tk.Toplevel):
    """Config Window of the application"""

    def __init__(self, appconfig: classes.config.Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig = appconfig
        self.title("Config")
        self.config(width=300, height=300)
        self.focus()
        self.grab_set()

        self.client_id_label = tk.Label(self, text="Client ID")
        self.client_id_label.grid(row=0, column=0)
        self.client_id_input = tk.Entry(self, width=30)
        self.client_id_input.grid(row=0, column=1)
        self.client_id_input.insert(0, self.appconfig.get_key("client_id"))

        self.client_secret_label = tk.Label(self, text="Client Secret")
        self.client_secret_label.grid(row=1, column=0)
        self.client_secret_input = tk.Entry(self, width=30)
        self.client_secret_input.grid(row=1, column=1)
        self.client_secret_input.insert(0, self.appconfig.get_key("client_secret"))

        self.user_agent_label = tk.Label(self, text="User Agent")
        self.user_agent_label.grid(row=2, column=0)
        self.user_agent_input = tk.Entry(self, width=30)
        self.user_agent_input.grid(row=2, column=1)
        self.user_agent_input.insert(0, self.appconfig.get_key("user_agent"))

        self.refresh_token_label = tk.Label(self, text="Refresh Token")
        self.refresh_token_label.grid(row=3, column=0)
        self.fr = self.appconfig.get_key("refresh_token")
        self.frbool = bool(self.fr)
        self.text = 'Yes' if self.frbool is True else 'No, click connect to connect'
        self.refresh_token_input = tk.Label(self, text=self.get_refresh_token_status())
        self.refresh_token_input.grid(row=3, column=1)

        self.save_button = tk.Button(self, text="Save & Close", command=self.on_save_button_click)
        self.save_button.grid(row=4, column=1)
        self.connect_button = tk.Button(self, text="Connect", command=self.on_connect_button_click)
        self.connect_button.grid(row=4, column=0)

    def on_save_button_click(self):
        """Saves the config"""
        self.appconfig.save_string("client_id", self.client_id_input.get())
        self.appconfig.save_string("client_secret", self.client_secret_input.get())
        self.appconfig.save_string("user_agent", self.user_agent_input.get())
        self.destroy()
        pass

    def on_connect_button_click(self):
        """Connects to reddit"""
        if self.client_id_input.get() == "":
            print("No client id entered")
            return
        if self.client_secret_input.get() == "":
            print("No client secret entered")
            return
        if self.user_agent_input.get() == "":
            print("No user agent entered")
            return
        self.appconfig.save_string("client_id", self.client_id_input.get())
        self.appconfig.save_string("client_secret", self.client_secret_input.get())
        self.appconfig.save_string("user_agent", self.user_agent_input.get())
        token = Reddit().get_refresh_token()
        self.appconfig.save_string("refresh_token", token)
        self.refresh_token_input['text'] = self.get_refresh_token_status()

    def get_refresh_token_status(self):
        self.fr = self.appconfig.get_key("refresh_token")
        print(self.fr)
        self.frbool = bool(self.fr)
        return 'Yes' if self.frbool is True else 'No, click connect to connect'