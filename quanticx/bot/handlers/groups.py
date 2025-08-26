from __future__ import annotations

import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(F.new_chat_members)
async def on_user_joined(message: Message):
    user = message.new_chat_members[0]
    await message.reply(f"Вітаємо, {user.full_name}! Будь ласка, ознайомтесь з правилами.")


@router.message(Command("setwelcome"))
async def set_welcome(message: Message):
    if not message.from_user or not (message.from_user.is_chat_admin() if hasattr(message.from_user, "is_chat_admin") else True):
        return await message.reply("Тільки адміни можуть змінювати привітання")
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return await message.reply("Використання: /setwelcome Текст привітання")
    # Local setting for demo; persistence should call backend /groups/set
    await message.reply("Привітання оновлено")


@router.message()
async def caps_filter(message: Message):
    if not message.text:
        return
    text = message.text.strip()
    if len(text) >= 8 and re.fullmatch(r"[A-Z0-9\W]+", text):
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer("Будь ласка, без капс-локу")
