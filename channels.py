from telethon.sync import TelegramClient
from telethon.tl.types import Channel, Chat

from info import api_id, api_hash

client = TelegramClient('session_name', api_id, api_hash)

async def list_all_chats():
    await client.start()
    dialogs = await client.get_dialogs()
    
    for dialog in dialogs:
        entity = dialog.entity
        if isinstance(entity, (Channel, Chat)):
            print(f"Name: {entity.title}")
            print(f"ID: {entity.id}")
            if hasattr(entity, 'username') and entity.username:
                print(f"Username: {entity.username}")
            print(f"Access Hash: {getattr(entity, 'access_hash', 'N/A')}")
            print("-" * 40)

with client:
    client.loop.run_until_complete(list_all_chats())
