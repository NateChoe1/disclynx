import discord
import subprocess

client = discord.Client()
shebang = '$disclynx '

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
    print(output_content)

    await message.channel.send('```\n' + output_content + '\n```')
    # This naive code block escape strategy is incredibly easy to fool, but I
    # really don't care.

secret_file = open("secrets.txt", "r")
client.run(secret_file.read())
