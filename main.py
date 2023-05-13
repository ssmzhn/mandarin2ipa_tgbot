"""
Copyright 2022-2022 Purofle and contributors.

此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 可以在以下链接找到该许可证.
Use of this source code is governed by the GNU AGPLv3 license that can be found through the following link.

https://www.gnu.org/licenses/gpl-3.0.html

运行需要传入API_TOKEN作为环境变量
"""
import hashlib
import json
import logging
import sys
from typing import Any, Dict
from random import sample

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from thefuzz import fuzz

import ipa
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=sys.argv[1])
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\n欢迎使用该 Bot! 请使用 inline 调用。\n")
@dp.inline_handler()
async def get_ipa(inline_query: InlineQuery):
    text = inline_query.query
    items = []
    for x,y in enumerate(ipa.select_table):
        result_id: str = hashlib.md5(y.encode()).hexdigest()
        items.append(
            InlineQueryResultArticle(
                id=result_id,
                title=y,
                input_message_content=InputTextMessageContent(y+":\n"+ipa.converted2string(text, mode=x)),
            )
        )
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
