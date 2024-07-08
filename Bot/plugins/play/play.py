from pyrogram import filters, Client
from pyrogram.types import Message

from Bot import app
from strings import get_command

PLAY_COMMAND = get_command("PLAY_COMMAND")


@app.on_message(filters.command(PLAY_COMMAND, prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def play(client: Client, message: Message):
    await message.reply("Play Command")
