from module.localConfig import TEL_HASH, TEL_ID

import asyncio
from telethon import TelegramClient, events


if __name__ == "__main__":
    client = TelegramClient('main', TEL_ID, TEL_HASH)
    client.start()
    client.run_until_disconnected()
    client.disconnect()
