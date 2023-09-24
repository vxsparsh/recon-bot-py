# RECON BOT
## Recon automation on VPS

Logging in into vps every time and running the commands manually one after another is a hectic task, so instead we’ll use this discord bot to automate the process, it will run on the same vps as the tools are installed on. It will execute and commands and return the result to us on our discord server.

## SETUP
There are a few things you need to install and setup before you can start using this script.

- A VPS (preferably Amazon Linux EC2 on AWS, because there seems to be problem when installing chromium on other distros such as ubuntu on a vps.)

- Discord BOT and Webhook

- Required Tools (subfinder, httpx and aquatone)

- Environment Variables

### VPS

Create a VPS and install python3-pip in it. It is recommended to use AWS EC2 Amazon Linux for this bot because it is tested on it and works fine.

```bash
sudo yum install python3-pip
```

### Discord BOT and Webhook

First create a new discord server.

To create a discord bot goto [Discord Developer Portal](https://discord.com/developers/applications) and create a new application, name it whatever you want then open that application and goto BOT section from the menu on the left, copy the bot token and save it somewhere because it is generated for one time use only. Invite the bot into your server.

To create webhooks, in your new discord server goto server settings>integrations>webhooks
Create 2 webhooks, one for subfinder and another for aquatone copy and save both webhook urls.

### Required Tools

3 tools are required for this bot to run: subfinder, httpx, aquatone and chromium (needed for aquatone)

```bash
wget https://github.com/projectdiscovery/httpx/releases/download/v1.3.5/httpx_1.3.5_linux_amd64.zip
wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip
wget https://github.com/projectdiscovery/subfinder/releases/download/v2.6.3/subfinder_2.6.3_linux_amd64.zip
```
This will download httpx, aquatone and subfinder.
Move these tools to /usr/local/bin after unzipping them.
```bash
sudo mv httpx /usr/local/bin
sudo mv aquatone /usr/local/bin
sudo mv subfinder /usr/local/bin
```

To install chromium refer to the following [blog post](https://cloud.google.com/looker/docs/best-practices/how-to-install-chromium-for-amazon-linux).

### Environment Variables
Now finally we need to configure the environment variables needed for the bot to function.
open .bashrc file in nano ```nano ~/.bashrc```
scroll to the bottom and add the following environment variables there...

```
export bot_token="<your discord bot token>"
export subfinder_command="subfinder"
export httpx_command="/usr/local/bin/httpx"
export aquatone_command="aquatone"
export subfinder_webhook="<your subfinder webhook url>"
export aquatone_webhook="<your aquatone webhook url>"
```
Replace the url and tokens with your own, its best to keep them all saved in one file just in case.
exit out of nano and do ```source ~/.bashrc``` for the changes to take immediate effect.
Type ```env``` to verify that the environment variables are working.

Now finally run the bot:
```python3 bot.py```

### BOT USAGE
Bot Commands can be viewed by typing `!help` in your discord server.