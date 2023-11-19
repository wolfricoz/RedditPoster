---
layout: default
title: Connect to Reddit
nav_order: 2
---
<h1 style="text-align: center">How to connect to reddit</h1>

* ### Create a Reddit Account:

If the user doesn't have a Reddit account, they need to sign up for one
at [Reddit's registration page](https://www.reddit.com/register).

* ### Create a Reddit App:

In order to use the Reddit API, the user needs to create a Reddit app. This is done by going
to [Reddit's App Preferences page and clicking](https://www.reddit.com/prefs/apps) on "Create App."

* ### Fill in the App Information:

The user selects the app type (preferably "script" for personal use).
Provide a name, description, and URLs for the app. The "redirect uri" should be a URL where the user's authentication
token will be sent. Use `http://localhost:8080`.

for user agent, use `<script name> by /u/<your reddit username>`

* ### Complete the Security Check:

Solve the CAPTCHA and click "Create app."

* ### Retrieve Client ID and Client Secret:

After creating the app, the user will see the app details page. Note down the "client ID" and "client secret." These
will be used in the authentication process.

* ### Fill the information in Reddit Poster:

Click on the Config Button and fill in the following information:
* Client ID (from the app details page)
* Client Secret (from the app details page)
* user agent: `<script name> by /u/<your reddit username>`
* interval: the interval between posts in seconds (recommended 5)

once you have filled in the information, click on the "Connect" button. This will open a browser window where you will
be asked to log in to your reddit account and authorize the app. Once you have done that, you will be redirected to a
page that says "all done!" You can close the browser window and go back to the app.

if the refresh token is successfully retrieved, the retresh token will be changed from No to Yes in the config window. 
This is a one time process. Once you have retrieved the refresh token, you can use it to post to reddit without having
to log in again.

![App Details](images/app_details.png)