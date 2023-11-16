import tkinter as tk

class RedditWindow:
    def __init__(self, appconfig: classes.config.Config, subreddit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig = appconfig
        self.name = subreddit
        self.title(f"{self.name} configuration")
        self.config(width=500, height=300)
        self.focus()
        # self.grab_set()

        self.subreddit_name = tk.Label(self, text=f"Subreddit name:")
        self.subreddit_name.grid(row=0, column=0, sticky="nsew")
        self.subreddit_name_input = tk.Entry(self)
        self.subreddit_name_input.grid(row=0, column=1, sticky="nsew")
        self.subreddit_name_input.insert(0, self.name)

        self.flair_text = tk.Label(self, text=f"Flair text:")
        self.flair_text.grid(row=1, column=0, sticky="nsew")

