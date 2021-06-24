from aiogram import types, Bot, executor, Dispatcher
import buttons
from weather_broadcast import WeatherBroadcast
from data_base import SQLighter
import asyncio


TOKEN = "1337329290:AAF1mQVdAPSgiNBANs39lng_4FsWtDVHtVE"

bot = Bot(TOKEN)
flag = False
dp = Dispatcher(bot)

db = SQLighter('database.db')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nЯ бот, делающий прогноз погоды\n'
                        'Для общения со мной используй кнопки внизу👇', reply_markup=buttons.start_kb)


@dp.message_handler(regexp='Изменить город')
async def process_change_city_command(message: types.Message):
    global flag
    flag = True
    await bot.send_message(message.from_user.id, "Введите название города на английском языке", reply_markup=buttons.cancel_kb)


@dp.message_handler(regexp='([A-Za-z])+')
async def process_city_name_command(message: types.Message):
    global flag
    if flag == False:
        return
    try:
        WeatherBroadcast(message.text).broadcast()
        if db.subscriber_exists(message.from_user.id):
            db.update_town(message.from_user.id, message.text)
        else:
            db.add_subcriber(message.from_user.id, message.text)
        flag = False
        await bot.send_message(message.from_user.id, "Город был успешно изменен", reply_markup=buttons.kb)
    except:
        await bot.send_message(message.from_user.id, 'Не удалось найти город😥\nПопробуйте еще раз', reply_markup=buttons.cancel_kb)


@dp.message_handler(regexp='Текущий город')
async def process_current_city_command(message: types.Message):
    if db.subscriber_exists(message.from_user.id):
        await bot.send_message(message.from_user.id, db.get_town(message.from_user.id))
    else:
        db.add_subcriber(message.from_user.id, "Moscow")
        await bot.send_message(message.from_user.id, db.get_town(message.from_user.id))


@dp.message_handler(regexp='Посмотреть прогноз')
async def process_current_temperature_command(message: types.Message):
    await bot.send_message(message.from_user.id, WeatherBroadcast(db.get_town(message.from_user.id)).broadcast())


@dp.message_handler(regexp='Отмена')
async def process_cancel_command(message: types.Message):
    global flag
    flag = False
    await bot.send_message(message.from_user.id, "Действие было отменено", reply_markup=buttons.kb)


@dp.message_handler(regexp='Рассылка')
async def process_mailing_command(message: types.Message):
    await bot.send_message(message.from_user.id, "ВАЖНО\nРассылка осуществляется ежечасно", reply_markup=buttons.mailing_kb)


@dp.message_handler(regexp='Подписаться')
async def process_subscribe(message: types.Message):
    if db.get_status(message.from_user.id):
        await bot.send_message(message.from_user.id, "Вы уже подписаны😉", reply_markup=buttons.kb)
    else:
        db.update_status(message.from_user.id)
        await bot.send_message(message.from_user.id, "Вы успешно подписались на рассылку!)", reply_markup=buttons.kb)


@dp.message_handler(regexp='Отписаться')
async def process_unsubcscribe(message: types.Message):
    if db.get_status(message.from_user.id) == False:
        await bot.send_message(message.from_user.id, "Вы и так не подписаны", reply_markup=buttons.kb)
    else:
        db.update_status(message.from_user.id, False)
        await bot.send_message(message.from_user.id, "Вы успешно отписались от рассылки", reply_markup=buttons.kb)


async def mailing(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        subs = db.get_subscriptions(True)
        for sub in subs:
            await bot.send_message(sub[1], WeatherBroadcast(sub[2]).broadcast())


if __name__ == '__main__':
    dp.loop.create_task(mailing(3600))
    executor.start_polling(dp)
