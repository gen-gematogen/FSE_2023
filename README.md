# FSE 2023 : Telegram Bot for Checkers
This repository is devoted to store our project: a telegram bot for playing checkers with a friend.
## Telegram Bot Initialization
In order to properly use our project, one has to create an empty Telegram Bot first.

In order to do so, please, follow [this link](https://t.me/BotFather) and create a new bot using the `\newbot` command.

Next, please, copy the bot's HTTP API token, so that to use it further.

## Environment Setup --- docker
```bash
chmod u+x docker_build.sh
chmod u+x docker_run.sh 
./build.sh
./run.sh
```
## Scripts for Testing
Once in the docker container, simply write:
```bash
./project_test.sh
```
And it will run all the tests using `pytest`, and show if they went successfully.
## Building the Project
To finally start the Telegram bot, please, run the following command:
```bash
./project_build.sh "YOUR_TELEGRAM_BOT_API"
```
with your own bot's api token put as the argument instead of `YOUR_TELEGRAM_BOT_API`. 
## Using the bot
Once the project is set up and connection is established, please, go to your Telegram Bot and set it up by typing `\start` in the input field.

After that you can properly play checkers! Remember to hand the phone to your friend at their turn :)
