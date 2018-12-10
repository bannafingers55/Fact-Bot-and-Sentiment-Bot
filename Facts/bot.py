import discord
import asyncio

import os
import sys
import inspect
import time
import random

from datetime import datetime
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#This is a bot designed to stop bad messages on a discord server, howerver I need to type it in first
blacklistedWords = ["nigger"]
exceptions = ["nice"]

f = open("facts.txt", "r")
facts = f.read()
f.close()
facts = facts.split("\n")

#Platform check
if os.name == "nt":
    print("Windows detected")
    os_name = "windows"

elif os.name == "posix":
    print("Unix detected")
    os_name = "unix"
else:
    print("Woh what os are you using??? This bot might have incompatabilities, it only supports unix and windows!")
    os_name = "unix"

#Discord Setup
class FilterBot(discord.Client):
    def __innit__(self):
        global shard_count
        version = "1.0"
        self.token()
        self.appinfo = ""
        self.owner = ""
        self.prefix = ">"
        super().__innit__(shard_id=0, shard_count=1)
        self._setup_logging()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        token = open("data/token.data", "r").read()
        loop = asyncio.get_event_loop()
        self.loop = loop
        try:
            loop.run_until_complete(self.start(token))
        finally:
            try:
                try:
                    self.loop.run_until_complete(self.logout())
                except:
                    pass
                pending = asyncio.Task.all_tasks()
                gathered = asyncio.gather(*pending)
                try:
                    gathered.cancel()
                    loop.run_until_complete(gathered)
                    gathered.exception()
                except:
                    pass
            except Exception as e:
                loop.close()

    async def cmd_ping(self, channel):
        t1 = time.perf_counter()
        await self.send_typing(channel)
        t2 = time.perf_counter()
        ping = (float(t2 - t1)) * 1000
        ping = round(ping, 0)
        ping = str(ping)
        ping = ping.replace(".0", "")
        em = discord.Embed(title="Ping", colour=(random.randint(0, 16777215)))
        em.set_thumbnail(url="http://i.imgur.com/L6sA5sd.png")
        em.add_field(name="Response time", value="{} ms.".format(ping), inline=True)
        await self.send_message(channel, embed=em)


    async def cmd_fact(self, channel):
        fact = random.choice(facts)
        em = discord.Embed(title="Fact", colour=(random.randint(0, 16777215)))
        em.set_thumbnail(url="https://image.shutterstock.com/image-vector/fun-fact-vector-illustration-on-260nw-740092852.jpg")
        em.add_field(name="Fact:", value="{}".format(fact), inline=True)
        await self.send_message(channel, embed=em)
        
    async def on_message(self, message):
      messageContent = message.content.split(" ")
      for i in messageContent:
        for j in blacklistedWords:
          if similar(i.lower(), j) >= 0.7 and i != "nice":
            await self.delete_message(message)
            await self.send_message(message.author, "Please refrain from using that word")
            chnl = discord.Object(id=521371994185531392)
            self.send_message(chnl, "{}: {}".format(message.author, message.content))

      for i in blacklistedWords:
            ctx = message.content.lower()
            if i in ctx and i != "nice":
              await self.delete_message(message)
              await self.send_message(message.author, "Please refrain from using that word")
              chnl = discord.Object(id=521371994185531392)
              self.send_message(chnl, "{}: {}".format(message.author, message.content))
              #await self.send_message("bannanafingers55#7368", "%s used a blacklisted word"%(message.author))
      msg = message.content
      if msg.startswith(">") == False:
          return

      command, *args = message.content.split(
          ' ')  # Uh, doesn't this break prefixes with spaces in them (it doesn't, config parser already breaks them)
      command = command[len('>'):].lower().strip()
      handler = getattr(self, 'cmd_' + command, None)
      if not handler:
          return
      print("{0.id}/{0!s}: {1}".format(message.author, message.content.replace('\n', '\n... ')))
      argspec = inspect.signature(handler)
      params = argspec.parameters.copy()
      sentmsg = response = None
      # noinspection PyBroadException
      #try:
      handler_kwargs = {}
      if params.pop('message', None):
          handler_kwargs['message'] = message
      if params.pop('channel', None):
          handler_kwargs['channel'] = message.channel
      if params.pop('author', None):
          handler_kwargs['author'] = message.author
      if params.pop('server', None):
          handler_kwargs['server'] = message.server
      if params.pop('permissions', None):
          handler_kwargs['permissions'] = user_permissions
      if params.pop('user_mentions', None):
          handler_kwargs['user_mentions'] = list(map(message.server.get_member, message.raw_mentions))
      if params.pop('channel_mentions', None):
          handler_kwargs['channel_mentions'] = list(map(message.server.get_channel, message.raw_channel_mentions))
      if params.pop('leftover_args', None):
          handler_kwargs['leftover_args'] = args
      args_expected = []
      for key, param in list(params.items()):
            # parse (*args) as a list of args
          if param.kind == param.VAR_POSITIONAL:
              handler_kwargs[key] = args
              params.pop(key)
              continue
          # parse (*, args) as args rejoined as a string
          # multiple of these arguments will have the same value
          if param.kind == param.KEYWORD_ONLY and param.default == param.empty:
              handler_kwargs[key] = ' '.join(args)
              params.pop(key)
              continue
          doc_key = '[{}={}]'.format(key, param.default) if param.default is not param.empty else key
          args_expected.append(doc_key)
          # Ignore keyword args with default values when the command had no arguments
          if not args and param.default is not param.empty:
              params.pop(key)
              continue
          # Assign given values to positional arguments
          if args:
              arg_value = args.pop(0)
              handler_kwargs[key] = arg_value
              params.pop(key)
      # Invalid usage, return docstring
      if params:
          docs = getattr(handler, '__doc__', None)
          if not docs:
              docs = 'Usage: {}{} {}'.format(
                  prefix,
                  command,
                  ' '.join(args_expected)
              )
          docs = dedent(docs)
          await self.safe_send_message(
              message.channel,
              '```\n{}\n```'.format(docs.format(command_prefix=prefix)),
              expire_in=60
          )
          return
      response = await handler(**handler_kwargs)
      if response and isinstance(response, Response):
          content = response.content
          if response.reply:
              content = '{}, {}'.format(message.author.mention, content)
          sentmsg = await self.safe_send_message(
              message.channel, content,
              expire_in=response.delete_after if self.config.delete_messages else 0,
              also_delete=message if self.config.delete_invoking else None
          )

    async def on_server_join(self, server):
        name = server.name
        msg = "Thanks for adding me to '{}', if you need help type >help , and have fun!".format(name)
        await self.send_message(server, msg)



    async def on_ready(self):
        # Boot logging
        self.appinfo = await self.application_info() #you can now get ALL your appinfo ##http://discordpy.readthedocs.io/en/latest/api.html#discord.AppInfo
        self.owner = self.appinfo.owner #you now always have an accurate owner object to use (this is a user object, e.g. self.owner.id, self.owner.name etc.
        now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Connected as " + str(self.user) + " at " + now + " on  servers!")

    """f = open('data/commands.data', 'a')
    for line in f:
        if line != "\n" or "":
            line_help = line + "_help"
            line_help = line_help.replace("\n", "")
            help_msg = eval(line_help)"""