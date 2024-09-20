from telethon import TelegramClient, events
import asyncio
import re
import os
import pytz
from signal_parser import parse_signal


api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
 

# List of channel usernames or invite links to monitor
channels_to_monitor = [
    'MasterofGold52',  # Replace with your channel's username without '@'
    # 'https://t.me/+V9JUuL1HTeo0YTBk',
    # Add more channels as needed
]
local_timezone = pytz.timezone('Etc/GMT-3')
# Create and initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def fetch_recent_messages():
    for channel in channels_to_monitor:
        try:
            entity = await client.get_entity(channel)
            print(f"\nFetching messages from: {entity.title} ({entity.username})")
            
            # Fetch the last 10 messages
            messages = await client.get_messages(entity, limit=10)
            
            for message in messages:
                # print(f" {message.text}")
                parsed_message = parse_signal(message.text)
                if parsed_message:
                    print(parsed_message)
                
        except Exception as e:
            print(f"Error fetching messages from {channel}: {e}")

@client.on(events.NewMessage(chats=channels_to_monitor))
async def new_message_handler(event):
    channel = await event.get_chat()
    message = event.message.message
    print(f"\nNew message in {channel.title}: {message}")
    
    # Here you can call your signal processing function
    # For example: process_signal(message)

async def main():
    await client.start()
    print("Client is running and connected to Telegram.")
    
    # Fetch recent messages
    await fetch_recent_messages()
    
    print("\nListening for new messages...")
    
    # Keep the script running to listen for new messages
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
