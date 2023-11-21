import os
import random
import socket
import sys
import webbrowser

import prawcore.exceptions
from praw.exceptions import PRAWException
import praw

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

class Reddit:
    def __init__(self):
        self.reddit: praw.reddit

    def get_refresh_token(self, config):
        try:
            client_id = config.get_key("client_id")
            client_secret = config.get_key("client_secret")
            commaScopes = "all"

            if commaScopes.lower() == "all":
                scopes = ["*"]
            else:
                scopes = commaScopes.strip().split(",")

            reddit = praw.Reddit(
                    client_id=client_id.strip(),
                    client_secret=client_secret.strip(),
                    redirect_uri="http://localhost:8080",
                    user_agent="praw_refresh_token_example",
            )
            state = str(random.randint(0, 65000))
            url = reddit.auth.url(scopes, state, "permanent")
            page = webbrowser.open(url, new=0, autoraise=True)
            sys.stdout.flush()
            client = receive_connection()
            data = client.recv(1024).decode("utf-8")
            param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
            params = {
                key: value for (key, value) in [token.split("=") for token in param_tokens]
            }

            if state != params["state"]:
                send_message(
                        client,
                        f"State mismatch. Expected: {state} Received: {params['state']}",
                )
                return 1
            elif "error" in params:
                send_message(client, params["error"])
                return 1

            refresh_token = reddit.auth.authorize(params["code"])
            send_message(client, f"Refresh token: {refresh_token}. You should NEVER share this code with anyone.\n\nyou can close this page now.")
            return refresh_token
        except Exception as e:
            print(e)
            if os.path.exists("logs") is False:
                os.mkdir("logs")
            with open("logs/error.txt", 'a') as f:
                f.write(str(e))

    def authorize(self, config):
        reddit = praw.Reddit(client_id=config.get_key("client_id"),
                             client_secret=config.get_key("client_secret"),
                             user_agent=config.get_key("user_agent"),
                             redirect_uri=config.get_key("redirect_uri"),
                             refresh_token=config.get_key("refresh_token"))
        return reddit

    def post_to_reddit(self, config, subreddit, title, body):
        """Posts to reddit"""
        reddit = self.authorize(config)

        reddit.validate_on_submit = True
        subredditinfo = config.config["subreddits"][subreddit]
        try:
            reddit.subreddit(subreddit).submit(title, selftext=body, flair_id=subredditinfo["flair_id"], nsfw=subredditinfo["nsfw"])
            return f"Successfully posted to {subreddit}", False
        except PRAWException as e:
            if config.get_key("auto_remove") is True:
                config.remove_subreddit(subreddit)
            return f"Failed to post to {subreddit} because of {str(e).split(':')[0]}, {'Removing subreddit from config' if config.get_key('auto_remove') is True else ''}", True
        except prawcore.exceptions.RequestException:
            return "Connection Error, check your internet connection", False

    def get_flairs(self, config, subreddit):
        """Gets flairs from subreddit"""
        try:
            flair_dict = {}
            reddit = self.authorize(config)
            flairs = list(reddit.subreddit(subreddit).flair.link_templates.user_selectable())
            for flair in flairs:
                flair_dict[flair['flair_text']] = flair['flair_template_id']
            if len(flair_dict) == 0:
                return ["No flairs found"]
            return flair_dict
        except prawcore.exceptions.RequestException:
            return ["Please connect to your account first"]
        except prawcore.exceptions.NotFound:
            return ["Subreddit not found"]
        except prawcore.exceptions.Forbidden:
            return ["Forbidden"]
        except Exception as e:
            return [str(e)]

def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        client = server.accept()[0]
        server.close()
        return client
    except Exception as e:
        print(e)
        if os.path.exists("logs") is False:
            os.mkdir("logs")
        with open("logs/weberror.txt", 'a') as f:
            f.write(str(e))


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()
