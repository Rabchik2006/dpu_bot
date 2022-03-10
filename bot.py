#!/bin/python3

# Libs
import json
import datetime, time
import asyncio
import os

from telethon import TelegramClient, events

# Variables
config_path = 'bot_config.json'
data_path='data.json'
none_data={'1':' ','2':' ','3':' ','4':' ','5':' ','6':' ','7':' ','8':' '}


# Read config
f = open(config_path, 'r')
conf = json.load(f)
f.close()



async def bot():
    async with TelegramClient('bot', conf['app_id'], conf['app_hash']) as tgclient:
        await tgclient.start()


        @tgclient.on(events.NewMessage(pattern='/send'))
        async def handler(event):
            with open('message_id.txt','w') as f:
                f.write(str(event.message.id+1))
            with open(data_path, 'r') as f:
                data = json.load(f)
            message=''
            for key in data.keys():
                message+=f'{key} - {data[key]}\n'
            await event.respond(message)


        @tgclient.on(events.NewMessage(pattern='/set'))
        async def handler(event):
            msg = event.message.message[5:].split(sep=' ')
            # print(msg)
            with open(data_path, 'r') as f:
                data = json.load(f)
            try:
                if data == none_data:
                    data={msg[0]:msg[1]}
                else:
                    data.update({msg[0]:msg[1]})
                with open(data_path, 'w') as f:
                    json.dump(data,f, indent=4)
            except:
                await event.reply('Неправильный индекс сообщения')
            await update_message()


        @tgclient.on(events.NewMessage(pattern='/delete'))
        async def handler(event):
            msg = event.message.message[8:]
            with open(data_path, 'r') as f:
                data = json.load(f)
            try:
                data.pop(msg)
            except:
                await event.reply('Неправильный индекс сообщения')
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=4)
            await update_message()


        @tgclient.on(events.NewMessage(pattern='/clear'))
        async def handler(event):
            with open(data_path,'w') as f:
                json.dump(none_data,f)
            await update_message()


        async def update_message():
            with open(data_path, 'r') as f:
                data = json.load(f)
            message = ''
            for key in data.keys():
                message += f'{key} - {data[key]}\n'
            with open('message_id.txt','r') as f:
                message_id=int(f.read())
            await tgclient.edit_message(await tgclient.get_entity('terraria_server_bot'), message_id, message)



        await tgclient.run_until_disconnected()


# User(id=1124695321, is_self=False, contact=False, mutual_contact=False, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False, access_hash=-1546900081710505395, first_name='Валерий', last_name='Рябченко', username='rabchik_engineer', phone=None, photo=UserProfilePhoto(photo_id=5397880207618193497, dc_id=2, has_video=False, stripped_thumb=None), status=UserStatusRecently(), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code='ru')

asyncio.run(bot())


