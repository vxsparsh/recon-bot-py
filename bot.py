import discord
import subprocess
import zipfile
import os
import shutil

TOKEN = os.getenv('bot_token')
SUBFINDER_COMMAND = os.getenv('subfinder_command')
HTTPX_COMMAND = os.getenv('httpx_command')
AQUATONE_COMMAND = os.getenv('aquatone_command')
SUBFINDER_WEBHOOK_URL = os.getenv('subfinder_webhook')
AQUATONE_WEBHOOK_URL = os.getenv('aquatone_webhook')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!enum'):
        domain = message.content.split(' ')[1]
        process = subprocess.Popen([SUBFINDER_COMMAND, '-d', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        subdomains = output.decode().split('\n')
        subdomains = [subdomain for subdomain in subdomains if subdomain]  # Remove empty lines

        count = len(subdomains)
        subdomains_text = '\n'.join(subdomains)

        response = f'Total subdomains found: {count}\n'
        response += f'Subdomains for {domain}:\n```{subdomains_text}```'

        await message.channel.send(response)

        # Save the subdomains to a file
        subdomains_file_path = f'{domain}_subdomains.txt'
        with open(subdomains_file_path, 'w') as file:
            file.write(subdomains_text)

        # Send subfinder results to Discord using the webhook
        subfinder_response = f'Subdomains for {domain}:\n```{subdomains_text}```'
        curl_command_subfinder = f'curl -X POST -H "Content-Type: multipart/form-data" -F "file=@{subdomains_file_path}" {SUBFINDER_WEBHOOK_URL}'
        subprocess.run(curl_command_subfinder, shell=True)

        # Probe subdomains using httpx tool and save the results
        httpx_results_file_path = f'{domain}_httpx_results.txt'
        httpx_command = f'{HTTPX_COMMAND} -l {subdomains_file_path} -o {httpx_results_file_path}'
        subprocess.run(httpx_command, shell=True)

        # Perform domain flyovers using Aquatone
        aquatone_command = f'cat {httpx_results_file_path} | {AQUATONE_COMMAND}'
        subprocess.run(aquatone_command, shell=True)

        # Create a ZIP archive of the specified folders and files
        zip_file_path = f'{domain}_aquatone_results.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for folder in ['headers', 'html', 'screenshots']:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.relpath(file_path, os.path.join(folder, '..')))

            for file in ['aquatone_report.html', 'aquatone_session.json', 'aquatone_urls.txt']:
                zipf.write(file, arcname=file)


        # Send the ZIP archive to Discord using the webhook
        curl_command_zip = f'curl -X POST -H "Content-Type: multipart/form-data" -F "file=@{zip_file_path}" {AQUATONE_WEBHOOK_URL}'
        subprocess.run(curl_command_zip, shell=True)

        # Cleanup the temporary files
        os.remove(subdomains_file_path)
        os.remove(httpx_results_file_path)
        os.remove(zip_file_path)

        for file in ['aquatone_urls.txt', 'aquatone_session.json', 'aquatone_report.html']:
            if os.path.exists(file):
                os.remove(file)

        for folder in ['screenshots', 'html', 'headers']:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    elif message.content.startswith('!notify'):
        mentioned_users = message.mentions
        if len(mentioned_users) == 0:
            await message.channel.send('Please mention a user to notify.')
            return

        notification_message = ' '.join(message.content.split(' ')[2:])

        for mentioned_user in mentioned_users:
            await mentioned_user.send(notification_message)

    elif message.content.startswith('!help'):
        # Create a Discord embed for the help message
        help_embed = discord.Embed(
            title='Bot Help',
            description='Commands and usage:',
            color=0x3498db  # You can customize the color here
        )
        help_embed.add_field(
            name='!enum <domain>',
            value='Enumerates subdomains for the specified domain.\nExample: `!enum hackthissite.org`',
            inline=False
        )
        help_embed.add_field(
            name='!notify <@user1> <@user2> ... <message>',
            value='Sends a notification message to mentioned users.\nExample: `!notify @User1 @User2 scan completed on example.com`',
            inline=False
        )
        help_embed.add_field(
            name='!help',
            value='Display this help message.',
            inline=False
        )

        await message.channel.send(embed=help_embed)

client.run(TOKEN)