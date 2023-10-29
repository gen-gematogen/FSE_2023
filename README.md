# FSE 2023 : Telegram Bot for Checkers
This repository is devoted to store our project: a telegram bot for playing checkers with a friend.
## Telegram Bot Initialization
In order to properly use our project, one has to create an empty Telegram Bot first.

In order to do so, please, follow [this link](https://t.me/BotFather) and create a new bot using the `\newbot` command.

Next, please, copy the bot's HTTP API token, so that to use it further.

## Environment Setup --- docker
```bash
chmod u+x build.sh
chmod u+x run.sh 
sh build.sh
sh run.sh
```
## Scripts for Testing
To run the tests in the docker container, simply write:
```bash
sh test.sh
```
And it will run all the tests.
## Building the Project
```bash
docker run -it checker_game:v1 python3 main.py - [API tg bot]
```
## Using the bot
Once the project is set up and connection is established, please, go to your Telegram Bot and set it up by typing `\start` in the input field.

After that you can properly play checkers! Remember to hand the phone to your friend at their turn :)
