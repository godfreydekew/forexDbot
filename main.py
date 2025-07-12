from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import asyncio
import re
from dotenv import load_dotenv
import os
import pytz
from signal_parser import parse_signal
from mt5_connect import MT5TradingBot
from info import password, account, server, api_id, api_hash

trading_bot = MT5TradingBot(account=account, password=password, server=server)

channel_id = 2487547787
access_hash = -8713634153597058688

channels_to_monitor = [
    InputPeerChannel(channel_id=channel_id, access_hash=access_hash)
]
local_timezone = pytz.timezone('Etc/GMT-3')
# Create and initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def fetch_recent_messages():
    for channel in channels_to_monitor:
        try:
            entity = await client.get_entity(channel)
            print(f"\nFetching messages from: {entity.title}")

            # Fetch the last 10 messages
            messages = await client.get_messages(entity, limit=10)

            for message in messages:
                print(f" {message.text}")
                parsed_message = parse_signal(message.text)
                if parsed_message:
                    print(parsed_message)
                    # trading_bot.place_trade(parsed_message)
        except Exception as e:
            print(f"Error fetching messages from {channel}: {e}")


@client.on(events.NewMessage(chats=channels_to_monitor))
async def new_message_handler(event):
    channel = await event.get_chat()
    message = event.message.message
    print(f"\nNew message in {channel.title}: {message}")
    parsed_message = parse_signal(message)

    # Check if the message contains a valid trade signal
    if parsed_message:
        print("Parsed signal:", parsed_message)
        trading_bot.place_trade(parsed_message)
    else:
        print("Message did not contain a valid trade signal.")

async def main():
    await client.start()
    print("Client is running and connected to Telegram.")

    await fetch_recent_messages()
    print("\nListening for new messages...")

    # Keep the script running to listen for new messages
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
