# A Smart yet Private Lamp Controller

## Motivation

Before you go to bed, you might need to go far away to turn off your bedroom light, and then go back in dark. Also, a nighttime urination could cause falls and injuries at night because your room is totally dark. How about using your phone to control your lamp switch? Indeed, you could download an app to control it. However, it might cause privacy leakage. HAHA, classic. Now, use the Python script to gain your private one. Also, if you use Telegram chat app, luckily, you can directly control your lamp without downloading any other app.


## Requirements

* Telegram App
* Python 3, install Python Telegram Bot
* A lamp that can be controled via HTTP. More specifically, the lamp need to accept a POST request and return a json object with keys, `what` and `auth`. The value of `what` is string `turn on` or `turn off`. 

## Get started

You need to build a file named `config.json`. It has several keys, `token`, `valid_user`, `url`, `auth`. The meanings and getting methods are as follows.

* Telegram officially supports users to build bots, and it helps users communicate with Telegram server. Search BotFather, build a new bot, and get your unique `token` for your bot.

* You do not want every Telegram user to control your lamp, right? You could use `valid_user` to store your unique Telegram user id. For example, `valid_user: ["123456789", "132456789"] `.

* Get `url` from your HTTP server.

* `auth` is the HTTP server authorization.