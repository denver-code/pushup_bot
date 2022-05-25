import os 
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from api.database import *

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, filters
from aiogram.utils import executor

API_TOKEN = os.getenv("token")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def user_exist(message):
    if await find_one_query("users", {"_id": message.from_user.id}):
        return True
    return False

@dp.message_handler(regexp=r"^[0-9]*$")
async def add_pushup_event(message: types.Message):
    if int(message.text) > 99999:
        message.tetx = "999"
    user = await find_one_query("users", {"_id": message.from_user.id})
    if len(user["statistics"]) > 0:
        if user["statistics"][-1]["day"] == date.today().day \
            and user["statistics"][-1]["month"] == date.today().month \
                and user["statistics"][-1]["year"] == date.today().year:
            user["statistics"][-1]["count"] += int(message.text)
        else:
            user["statistics"].append({
                "count": int(message.text),
                "day": date.today().day,
                "month": date.today().month,
                "year": date.today().year
            })
    else:
        user["statistics"].append({
            "count": int(message.text),
            "day": date.today().day,
            "month": date.today().month,
            "year": date.today().year
        })
    await update_db("users", {"_id": message.from_user.id}, user)
    await message.answer(f'Awesome!\nToday you pushed-up {user["statistics"][-1]["count"]} times')




@dp.message_handler(commands=["start"])
async def start_event(message: types.Message):
    if not await user_exist(message):
        await insert_db("users", {
            "_id": message.from_user.id,
            "statistics": []
        })
    await message.answer("""
Welcome in Push-up bot!
Here you can manage your push-up count and see statistics.

For start using - simple send count(number only) of your push-up's
Also you can see statistis after using this commands:
/all - show all information
/month - show month info
/yesterday - show yesterday info
/today - show current day info
""")

@dp.message_handler(commands=["today"])
async def today_event(message: types.Message):
    user = await find_one_query("users", {"_id": message.from_user.id})
    if len(user["statistics"]) > 0:
        if user["statistics"][-1]["day"] == date.today().day \
            and user["statistics"][-1]["month"] == date.today().month \
                and user["statistics"][-1]["year"] == date.today().year:
            return await message.answer(f'Today you pushed-up {user["statistics"][-1]["count"]} times')
    await message.answer("Sorry I don't have information :/")


@dp.message_handler(commands=["yesterday"])
async def yesterday_event(message: types.Message):
    user = await find_one_query("users", {"_id": message.from_user.id})
    if len(user["statistics"]) > 0:
        if user["statistics"][-1]["day"] == date.today().day \
            and user["statistics"][-1]["month"] == date.today().month \
                and user["statistics"][-1]["year"] == date.today().year:
            return await message.answer(f'Yesterday you pushed-up {user["statistics"][-2]["count"]} times')
        else:
            return await message.answer(f'Yesterday you pushed-up {user["statistics"][-1]["count"]} times')
    await message.answer("Sorry I don't have information :/")


@dp.message_handler(commands=["all"])
async def all_event(message: types.Message):
    user = await find_one_query("users", {"_id": message.from_user.id})
    if len(user["statistics"]) > 0:
        total_days = len(user["statistics"])
        count = 0
        for i in user["statistics"]:
            count += i["count"]
        return await message.answer(f"""
Total Information:
You pushed-up {count} times by {total_days} days
""")
    await message.answer("Sorry I don't have information :/")


@dp.message_handler(commands=["month"])
async def month_event(message: types.Message):
    user = await find_one_query("users", {"_id": message.from_user.id})
    if len(user["statistics"]) > 0:
        total_days = 0
        count = 0
        for i in user["statistics"]:
            if i["month"] == date.today().month \
                and i["year"] == date.today().year:
                    count += i["count"]
                    total_days += 1

        return await message.answer(f"""
Total Information by this month:
You pushed-up {count} times by {total_days} days
""")
    await message.answer("Sorry I don't have information :/")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)