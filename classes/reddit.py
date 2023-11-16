import random
import socket
import sys
import webbrowser

import prawcore.exceptions
from praw.exceptions import PRAWException
import praw


class Reddit:
    def __init__(self):
        self.reddit: praw.reddit

    def get_refresh_token(self):

        client_id = self.config.get_key("client_id")
        client_secret = self.config.get_key("client_secret")
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
        send_message(client, f"Refresh token: {refresh_token}, you can close this page now.")
        return refresh_token

    def post_to_reddit(self, config, subreddit, title, body):
        """Posts to reddit"""
        reddit = praw.Reddit(client_id=config.get_key("client_id"),
                             client_secret=config.get_key("client_secret"),
                             user_agent=config.get_key("user_agent"),
                             redirect_uri=config.get_key("redirect_uri"),
                             refresh_token=config.get_key("refresh_token"))

        reddit.validate_on_submit = True
        try:
            reddit.subreddit(subreddit).submit(title, selftext=body)
            return f"Successfully posted to {subreddit}"
        except PRAWException as e:
            print(e)
            config.remove_subreddit(subreddit)
            return f"Failed to post to {subreddit} because of {str(e).split(':')[0]}, Removing subreddit from config"
        except prawcore.exceptions.RequestException:
            return "Connection Error, check your internet connection"


def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()
