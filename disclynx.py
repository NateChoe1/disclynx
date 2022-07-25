import discord
import subprocess

client = discord.Client()
shebang = '$disclynx '
max_len = 2000

@client.event
async def on_ready():
    print('We have logged in as (0.user)'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(shebang):
        return

    url = message.content[len(shebang):]
    print('User has requested url %s' % (url))
    output_process = subprocess.run(['lynx', '-dump', url],
            stdout=subprocess.PIPE)
    output_content = output_process.stdout.decode('utf-8')

    await send_long_message(message.channel, output_content)

async def send_long_message(channel, message):
    current_message = ""
    lines = message.split('\n')
    for line in lines:
        if len(line) >= 2000:
            for i in range(0, len(line), 2000):
                await channel.send(message[i:i + min(2000, len(message - i))])
            continue
        elif len(current_message) + len(line) >= 2000:
            await channel.send(current_message)
            current_message = ""
        current_message = current_message + line + '\n'
    await channel.send(current_message)

secret_file = open("secrets.txt", "r")
client.run(secret_file.read())
