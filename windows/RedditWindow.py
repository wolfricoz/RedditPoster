import tkinter as tk
from tkinter import *

from classes.config import Config
from classes.reddit import Reddit


class RedditWindow(tk.Toplevel):
    def __init__(self, appconfig: Config, subreddit, rlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig = appconfig
        self.name = subreddit
        self.reddit_list = rlist
        self.title(f"{self.name} configuration")
        self.config(width=500, height=300)
        self.resizable(False, False)
        self.focus()
        # self.grab_set()

        self.subreddit_name = tk.Label(self, text=f"Subreddit name:")
        self.subreddit_name.grid(row=0, column=0, pady=2, padx=5,  sticky="nsew")
        self.subreddit_name_input = tk.Entry(self)
        self.subreddit_name_input.grid(row=0, column=1, pady=2, padx=5, sticky="nsew")
        self.subreddit_name_input.insert(0, self.name)

        self.flair_text = tk.Label(self, text=f"Flair text:")
        self.flair_text.grid(row=1, column=0, pady=2, padx=5, sticky="nsew")
        self.flairs = Reddit().get_flairs(self.appconfig, self.name)

        configflair = self.appconfig.config["subreddits"][subreddit]["flair_name"]
        if len(configflair) <= 1:
            configflair = list(self.flairs)[0]

        self.flair_text_input = tk.OptionMenu(self, tk.StringVar(value=configflair), *self.flairs)
        self.flair_text_input.grid(row=1, column=1, pady=2, padx=5, sticky="nsew")

        self.nsfw_toggle = tk.Label(self, text=f"NSFW?")
        self.nsfw_toggle.grid(row=2, column=0, pady=2, padx=5, sticky="nsew")
        self.nsfw_toggle = tk.Checkbutton(
                self,
                text="NSFW?",
                command=self.checkbox_nsfw)
        self.nsfw_toggle.grid(row=2, column=1, pady=2, padx=5, sticky="nsew")
        if self.appconfig.config["subreddits"][subreddit]["nsfw"] is True:
            self.nsfw_toggle.toggle()

        self.save_button = tk.Button(self, text="Save & Close", command=self.on_save_button_click)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")

    def checkbox_nsfw(self):
        self.appconfig.toggle_subreddit(self.name, "nsfw")

    def on_save_button_click(self):
        """Saves the config"""
        if self.subreddit_name_input.get() != self.name:
            self.appconfig.rename_subreddit(self.name, self.subreddit_name_input.get())
            self.name = self.subreddit_name_input.get()
            self.update_list()
        currentflair = self.flair_text_input.cget("text")
        if currentflair == "":
            self.destroy()
            return
        try:
            self.appconfig.update_subreddit(self.name, currentflair, self.flairs.get(currentflair))
        except AttributeError:
            self.destroy()
        self.destroy()
        pass

    def update_list(self):
        self.reddit_list.delete(0, END)
        self.reddit_list.insert(END, *self.appconfig.get_subreddits())
