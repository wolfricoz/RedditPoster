import os.path
import queue
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import *

from classes.config import Config
from classes.reddit import Reddit
from windows.ConfigWindow import ConfigWindow
from windows.PostWindow import PostWindow
from windows.RedditWindow import RedditWindow


# https://www.geeksforgeeks.org/right-click-menu-using-tkinter/
# create a right click window
# configure double clicking an item in the listbox to open the reddit config window


class MainWindow:
    """Main Window of the application"""

    def __init__(self, master: tk.Tk):
        # Load the config and set variabes
        self.config = Config("config/config.json")
        self.config.update_config()
        self.subreddits = self.config.get_subreddits()
        # Settings of the main window
        self.master = master
        self.master.title("Main Window")
        # self.master.resizable(False, False)
        self.thread_queue = queue.Queue()

        self.frame = tk.Frame(self.master)

        # Create the menu
        self.m = Menu(self.master, tearoff=0)
        self.m.add_command(label="edit", command=self.open_RedditWindow)
        self.m.add_command(label="delete", command=self.on_remove_button_click)

        # Create the widgets

        self.reddit_entry = tk.Entry(self.frame)
        self.reddit_add_button = tk.Button(self.frame, text="Add subreddit", command=self.on_add_button_click)
        self.subreddits_title = tk.Label(self.frame, text="Subreddits")
        self.reddit_list = tk.Listbox(self.frame)
        self.reddit_remove_button = tk.Button(self.frame, text="Remove subreddit", command=self.on_remove_button_click)
        self.title_input = tk.Entry(self.frame)
        self.title_title = tk.Label(self.frame, text="Title")
        self.body_title = tk.Label(self.frame, text="Body")
        self.body_input = tk.Text(self.frame, wrap=WORD)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.body_input.yview, orient=VERTICAL, width=20)
        self.body_input['yscrollcommand'] = self.scrollbar.set

        self.post_button = tk.Button(self.frame, text="Post", command=self.on_post_button_click)
        self.config_button = tk.Button(self.frame, text="Config", command=self.on_config_button_click)
        self.help_button = tk.Button(self.frame, text="Help", command=lambda: webbrowser.open("https://wolfricoz.github.io/redditposterdocs/"))

        # Place the widgets
        # listbox
        self.reddit_entry.grid(row=1, column=0, padx=(10, 0), sticky='nsew')
        self.subreddits_title.grid(row=2, column=0, columnspan=2, pady=2, sticky='nsew')
        self.reddit_list.grid(row=3, column=0, rowspan=3, columnspan=2, padx=10, sticky='nsew')
        # Title
        self.title_title.grid(row=0, column=2, columnspan=3, sticky='nsew')
        self.title_input.grid(row=1, column=2, columnspan=3, padx=(10, 0), sticky='nsew')
        # Body
        self.body_title.grid(row=2, column=2, columnspan=3, pady=2, sticky='nsew')
        self.body_input.grid(row=3, column=2, rowspan=3, columnspan=3, padx=(10, 0), sticky='nsew')
        self.scrollbar.grid(row=3, column=5, rowspan=3, sticky='nsew')
        # Buttons
        self.reddit_add_button.grid(row=1, column=1, padx=(1, 10), sticky='nsew')
        self.reddit_remove_button.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='nsew')
        self.help_button.grid(row=6, column=2, padx=10, pady=(5, 10), sticky='nsew')
        self.config_button.grid(row=6, column=3, padx=10, pady=(5, 10), sticky='nsew')
        self.post_button.grid(row=6, column=4, padx=10, pady=(5, 10), sticky='nsew')
        self.frame.pack(fill=BOTH, expand=True)
        # insert the data into the appropriate widgets
        self.reddit_list.insert(END, *self.subreddits)
        if self.config.get_key("title") != "":
            self.title_input.insert(END, self.config.get_key("title"))

        if self.config.get_key("body") != "":
            self.body_input.insert(END, self.config.get_key("body"))

        # Configures the grid sizes if the window is resized
        rows = 6
        columns = 6
        for i in range(rows):
            if i in [0,1,2 , 4]:
                self.frame.grid_rowconfigure(i, weight=0)
                continue
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(columns):
            if i in [0, 1, 5]:
                self.frame.grid_columnconfigure(i, weight=0)
                continue
            self.frame.grid_columnconfigure(i, weight=1)

        self.save_post()
        self.listen_for_result()
        self.reddit_list.bind("<Double-Button-1>", lambda x: RedditWindow(self.config, self.reddit_list.get(self.reddit_list.curselection()), self.reddit_list))
        self.reddit_list.bind("<Button-3>", self.right_click)
        self.reddit_entry.bind("<Return>", lambda x: self.on_add_button_click())

    def save_post(self):
        """Saves the post to a file"""
        self.config.save_string("title", self.title_input.get())
        self.config.save_string("body", self.body_input.get("1.0", END))
        self.master.after(30000, self.save_post)

    def update_list(self):
        self.reddit_list.delete(0, END)
        self.reddit_list.insert(END, *self.config.get_subreddits())

    def on_add_button_click(self):
        """Adds a subreddit to the list and config"""
        if self.reddit_entry.get() == "":
            return
        if self.reddit_entry.get() in self.config.get_subreddits():
            return
        self.config.add_subreddit(self.reddit_entry.get())
        self.update_list()
        self.reddit_entry.delete(0, END)

    def on_remove_button_click(self):
        """Removes a subreddit from the list and config"""
        if len(self.reddit_list.curselection()) == 0:
            print("No subreddit selected")
            return
        self.config.remove_subreddit(self.reddit_list.get(self.reddit_list.curselection()))
        self.reddit_list.delete(0, END)
        self.reddit_list.insert(END, *self.config.get_subreddits())

    def on_config_button_click(self):
        """Opens the config window"""
        self.open_config_window = ConfigWindow(self.config)

    def write_to_log(self, result):
        option = 'a'
        if os.path.exists("logs/post.txt") is False:
            option = 'w'
            if os.path.exists("logs") is False:
                os.mkdir("logs")
        with open("logs/post.txt", option) as f:
            f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}: {result}")

    def on_post_button_click(self):
        """Posts to reddit"""
        self.window = PostWindow(self.config)
        self.window.show_cancel_button()
        threading.Thread(target=self.create_queue).start()

        self.window.show_close_button()
        self.update_list()

    def create_queue(self):
        for subreddit in self.config.get_subreddits():
            time.sleep(self.config.get_key("interval"))
            self.thread_queue.put(threading.Thread(target=self.create_post, args=(subreddit, self.window)).start())

    def create_post(self, subreddit, window: PostWindow):
        try:
            if not self.window.winfo_exists():
                print("cancelling")
                return
        except:
            self.write_to_log(f"Post to {subreddit} cancelled")
            return
        result, refresh = Reddit().post_to_reddit(self.config, subreddit, self.title_input.get(), self.body_input.get("1.0", END))
        if refresh:
            self.update_list()
        self.write_to_log(result)
        self.window.add_log(result)
        return result

    def listen_for_result(self):
        """ Check if there is something in the queue. """
        try:
            self.thread_queue.get(timeout=0)
            self.master.after(100, self.listen_for_result)
        except queue.Empty:
            self.master.after(10000, self.listen_for_result)

    def right_click(self, event):
        self.reddit_list.selection_clear(0, tk.END)
        self.reddit_list.selection_set(self.reddit_list.nearest(event.y))
        self.reddit_list.activate(self.reddit_list.nearest(event.y))
        self.m.post(event.x_root, event.y_root)


    def open_RedditWindow(self):
        self.reddit_window = RedditWindow(self.config, self.reddit_list.get(self.reddit_list.curselection()), self.reddit_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
