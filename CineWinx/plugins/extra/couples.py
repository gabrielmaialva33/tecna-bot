import os
import random
from datetime import datetime

from CineWinx.utils import save_couple, get_couple
from CineWinx.utils.database.couples_db import _get_image
from config import BANNED_USERS, PREFIXES
from strings import get_command
from telegraph import upload_file
from PIL import Image, ImageDraw
from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import *

from CineWinx import app as app

POLICE = [
    [
        InlineKeyboardButton(
            text="𓊈𒆜彡[𝐂𝐈𝐍𝐄𝐖𝐈𝐍𝐗™]彡𒆜𓊉",
            url=f"https://t.me/cinewinx",
        ),
    ],
]


def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


tomorrow = str(dt_tom())
today = str(dt()[0])

COUPLE_COMMAND = get_command("COUPLE_COMMAND")


@app.on_message(filters.command(COUPLE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("🚫 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝘀𝗼́ 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀.")
    try:
        is_selected = await get_couple(cid, today)
        if not is_selected:
            msg = await message.reply_text("🖼️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗼 𝗰𝗮𝘀𝗮𝗹...")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)

            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)

            photo1 = (await app.get_chat(c1_id)).photo
            photo2 = (await app.get_chat(c2_id)).photo

            n1 = (await app.get_users(c1_id)).mention
            n2 = (await app.get_users(c2_id)).mention

            try:
                p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
            except Exception:
                p1 = "assets/upic.png"
            try:
                p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
            except Exception:
                p2 = "assets/upic.png"

            img1 = Image.open(f"{p1}")
            img2 = Image.open(f"{p2}")

            img = Image.open("assets/cppic.png")

            img1 = img1.resize((380, 388))
            img2 = img2.resize((380, 388))

            mask = Image.new("L", img1.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + img1.size, fill=255)

            mask1 = Image.new("L", img2.size, 0)
            draw = ImageDraw.Draw(mask1)
            draw.ellipse((0, 0) + img2.size, fill=255)

            img1.putalpha(mask)
            img2.putalpha(mask1)

            draw = ImageDraw.Draw(img)

            img.paste(img1, (120, 195), img1)
            img.paste(img2, (510, 195), img2)

            img.save(f"cache/test_{cid}.png")

            txt = f"""
💑 <b>𝗖𝗮𝘀𝗮𝗹 𝗱𝗼 𝗗𝗶𝗮 𝗱𝗲 𝗛𝗼𝗷𝗲:</b>

{n1} + {n2} = 💚💘

📅 <b>𝗢𝘀 𝗽𝗿𝗼́𝘅𝗶𝗺𝗼𝘀 𝗰𝗮𝘀𝗮𝗶𝘀 𝘀𝗲𝗿𝗮̃𝗼 𝘀𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗮𝗱𝗼𝘀 𝗲𝗺 {tomorrow} !!</b>
"""

            await message.reply_photo(
                f"cache/test_{cid}.png",
                caption=txt,
                reply_markup=InlineKeyboardMarkup(POLICE),
            )
            await msg.delete()
            a = upload_file(f"cache/test_{cid}.png")
            for x in a:
                img = "https://graph.org/" + x
                couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(cid, today, couple, img)
        elif is_selected:
            msg = await message.reply_text("🖼️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗼 𝗰𝗮𝘀𝗮𝗹...")
            b = await _get_image(cid)
            # is_selected {'c1_id': 861801443, 'c2_id': 6762147109}
            c1_id = is_selected["c1_id"]
            c2_id = is_selected["c2_id"]

            user_1 = await app.get_users(c1_id)
            user_2 = await app.get_users(c2_id)

            c1 = user_1.mention
            c2 = user_2.mention

            txt = f"""
💑 <b>𝗖𝗮𝘀𝗮𝗹 𝗱𝗲 𝗛𝗼𝗷𝗲:</b>

{c1} + {c2} = 💚💘

📅 <b>𝗢𝘀 𝗽𝗿𝗼́𝘅𝗶𝗺𝗼𝘀 𝗰𝗮𝘀𝗮𝗶𝘀 𝘀𝗲𝗿𝗮̃𝗼 𝘀𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗮𝗱𝗼𝘀 𝗲𝗺 {tomorrow} !!</b>
"""

            await message.reply_photo(
                b, caption=txt, reply_markup=InlineKeyboardMarkup(POLICE)
            )
            await msg.delete()

    except Exception as e:
        print(str(e))

    try:
        os.remove(f"./downloads/pfp1.png")
        os.remove(f"./downloads/pfp2.png")
        os.remove(f"cache/test_{cid}.png")
    except Exception:
        pass


__MODULE__ = "💑 𝗖𝗮𝘀𝗮𝗹"
__HELP__ = """
📌 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗮𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗰𝗿𝗶𝗮𝗿 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗲 𝗰𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼. 𝗖𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗲́ 𝘂𝗺𝗮 𝗳𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮 𝗽𝗮𝗿𝗮 𝗰𝗿𝗶𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀 𝗯𝗲𝗹𝗮𝘀 𝗱𝗲 𝗰𝗼́𝗱𝗶𝗴𝗼 𝗳𝗼𝗻𝘁𝗲.

• /couples: 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗰𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗮𝗼 𝗴𝗿𝘂𝗽𝗼 𝗱𝗲 𝗰𝗵𝗮𝘁 𝗲 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝗰𝗼𝗻𝘁𝗲𝘂́𝗱𝗼 𝗱𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺.
"""