import asyncio
import os
import time
import tkinter as tk
import webbrowser
from tkinter import *
import classes.config
from classes.reddit import Reddit

class PostWindow(tk.Toplevel):

    def __init__(self, appconfig: classes.config.Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig = appconfig
        self.title("Post Log")
        self.config(width=500, height=300)
        self.focus()
        # self.grab_set()

        self.post_log = tk.Listbox(self, width=75, height=15)
        self.post_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.show_log = tk.Button(self, text="Open Log File", width=20, command=lambda : os.startfile(os.getcwd() + "/logs/post.txt"))
        self.show_log.grid(row=1, column=0, pady=10, sticky="N")

    def add_log(self, log: str):
        self.post_log.insert(END, log)
        self.post_log.see(END)
        self.update()
        pass

    def show_close_button(self):
        self.close_button = tk.Button(self, text="Close", command=self.on_close_button_click, width=20)
        self.close_button.grid(row=1, column=1, pady=10, sticky="N")

    def on_close_button_click(self):
        self.destroy()
        pass


