from aiogram import Bot, types, Dispatcher, executor
import sqlite3
import asyncio
#слито в @smoke_software
API_TOKEN = "5169282150:AAGf_Tioj59IsekGSg07ktT_aynKoaIioqM"
bot = Bot(token=API_TOKEN, parse_mode="html")
dp = Dispatcher(bot)

admin = [827638161]
with sqlite3.connect('data.db', check_same_thread=False) as connection:
    q = connection.cursor()


async def sep(num, sep):
    number = [str(num)[::-1][i:i + 3][::-1] for i in range(0, len(str(num)), 3)]
    m = f'{sep}'.join(number[::-1])
    return m


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        q.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    win INTEGER,
    eng INTEGER,
    kng INTEGER
    )""")
        q.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id}")
        result = q.fetchall()
        if len(result) == 0:
            q.execute(f"INSERT INTO users (user_id, win, lvl, eng, kng)"
                      f"VALUES ('{message.from_user.id}', '1000','1', '100', '5')")
            connection.commit()
            await message.answer('Здарова я игровой бот\n/help - Каталог команд')
        else:
            await message.answer('Здарова, игроман, я игровой бот\nСписок моих команд - /help')
    except Exception as error:
        await message.answer(f'Ошибка:\n{error}')


@dp.message_handler(commands=['bonus'])
async def me(message: types.Message):
    try:
        z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
        connection.commit()
        wins = z[0]
        if wins > int(1):
            await message.answer(f'Бонус можно получить если баланс = 1 монете, ваш баланс {wins}')

        else:
            q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(10000, message.from_user.id))
            await message.answer('Вы получили бонус в размере 10000 монет')
    except:
        await message.answer('Вас нету в базе\nТык --> /start')


@dp.message_handler(commands=['me'])
async def me(message: types.Message):
    try:
        z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
        x = q.execute(f'SELECT lvl FROM users WHERE user_id = {message.from_user.id}').fetchone()

        connection.commit()
        wins = z[0]
        lvls = x[0]
        await message.answer(
            f'Вот твои данные\n🆔: {message.from_user.id}\n\n🗓 Имя: {message.from_user.first_name}\n\n💰 Монет: {sep(round(wins), ".")}\n\n🔰 Уровень: {lvls}\n')

    except Exception as error:
        await message.answer(f'Ошибка:\n{error}')


@dp.message_handler(commands=['help'])
async def me(message: types.Message):
    await message.answer(
        '/top - Топ 10 богатых людей в боте\n/me - Ваш аккаунт\n/start - Запустить бота\n<b>/bonus - « получить бонус »,</b> если меньше 1 монет\n<b>Передать</b>, « сумма » - передать монеты ответом на сообщение\n<b>Передать</b>, « юзер ид », « Сумма »\n<b>Футбол - « сумма »</b>\n<b>Боулинг</b> - « сумма\n<b>Баскетбол</b> « Сумма »\n<b>Баланс</b>, Ваш баланс\n<b>Магазин</b> - прокачка, товары в боте\n\nКоманды с определенного уровня:\n<b>Дартс</b> « Сумма »\n<b>Казино</b> « Сумма » \n<b>Бандит</b> - « сумма »')


@dp.message_handler(commands=['balance'])
async def dick(message: types.Message):
    try:
        z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
        connection.commit()
        wins = z[0]
        await message.answer(f'💰 Ваш баланс {sep(round(wins), ".")}')
    except Exception as error:
        await message.answer(f'Ошибка:\n{error}')


@dp.message_handler(commands=['top'])
async def dighjkck(message: types.Message):
    try:
        q.execute("SELECT user_id, win FROM users order by win desc")
        res = q.fetchall()
        em = {0: '0', 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10"}
        message_lines = []
        for index, item in enumerate(res, 1):
            message_lines.append(f"{em.get(index)}. [{'Игрок'}](tg://openmessage?user_id={item[0]}): {item[1]} 💰")
        am = message_lines[:10]
        mes = '\n'.join(am)
        await message.answer(f'Список лидеров всего мира:\n\n{mes}', parse_mode='Markdown')
    except:
        await message.answer('ошибка')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.lower().startswith("боулинг"):
        try:
            z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
            connection.commit()
            wins = z[0]
            s = message.text.replace('.', '')
            word = s.replace('боулинг', '').split(" ", 1)
            if wins < int(word[1]):
                await message.answer('Баланс слишком низкий')
            else:
                dice_mes = await bot.send_dice(message.chat.id, '🎳')
                value = dice_mes.dice.value
                if value == 1:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1])}'
                    await message.answer(f"Мимо! <b>-{sep(djeks, '.')}</b> Монет. Попробуй еще раз\n")
                    q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()
                if value == 2:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1])}'
                    await message.answer(f"Увы ты сбил 1, <b>-{sep(djeks, '.')}</b> Монет. Попробуй еще раз\n")
                    q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()
                if value == 3:
                    await asyncio.sleep(4)
                    djeksx = f'{int(word[1]) * 1}'
                    await message.answer(f"Поздравляю, ты сбил целых 3 кегли, <b>+{sep(djeksx, '.')}</b> Монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeksx, message.from_user.id))
                    connection.commit()

                if value == 4:
                    await asyncio.sleep(4)
                    djeksx = f'{int(word[1]) * 2}'
                    await message.answer(f"Поздравляю, ты сбил целых 4 кегли, <b>+{sep(djeksx, '.')}</b> Монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeksx, message.from_user.id))
                    connection.commit()
                if value == 5:
                    await asyncio.sleep(4)
                    djeksx = f'{int(word[1]) * 3}'
                    await message.answer(f"Поздравляю, ты сбил целых 5 кегли, <b>+{sep(djeksx, '.')}</b> Монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeksx, message.from_user.id))
                    connection.commit()
                if value == 6:
                    await asyncio.sleep(4)

                    djeksx = f'{int(word[1]) * 4}'
                    await message.answer(f"Поздравляю, ты сбил все кегли, <b>+{sep(djeksx, '.')}</b> Монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeksx, message.from_user.id))
                    connection.commit()
        except Exception as error:
            await message.answer(f'Ошибка:\n{error}')

    if message.text.lower().startswith("футбол"):
        try:
            z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
            connection.commit()
            wins = z[0]
            s = message.text.replace('.', '')
            word = s.replace('/футбол -', ' ').split(" ", 1)
            if wins < int(word[1]):
                await message.answer('Баланс слишком низкий')
            else:
                dice_mes = await bot.send_dice(message.chat.id, '⚽️')
                value = dice_mes.dice.value
                if value in [1, 2]:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1])}'
                    await message.answer(f"Мимо! <b>-{sep(djeks, '.')}</b> Монет. Попробуй еще раз\n")
                    q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()

                if value in [3, 4, 5]:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1]) * 3}'
                    await message.answer(f"Поздравляю, ты забил гол! <b>+{sep(djeks, '.')} </b> монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()

        except Exception as error:
            await message.answer(f'Ошибка:\n{error}')

    if message.text.lower().startswith('передать'):
        if message.from_user.id in admin:
            try:
                if message.reply_to_message:
                    s = message.text.replace('.', '').replace('.', '')
                    word = s.replace('передать -', '').split(" ", 1)

                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(word[1],
                                                                                          message.reply_to_message.from_user.id))
                    connection.commit()
                    await message.answer(
                        f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a> Передал {sep(word[1], ".")}  монет для <a href="tg://openmessage?user_id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>')
                if not message.reply_to_message:
                    sx = message.text.replace('.', '')
                    wordx = sx.replace('передать', '').split(" ", 2)
                    wordsx = sx.replace('передать', '').split(" ", 3)
                    s = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
                    connection.commit()
                    wins = s[0]
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(wordsx[2], wordx[1]))
                    connection.commit()
                    await message.answer(
                        f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a> Передал {sep(wordsx[2], ".")}  монет для <a href="tg://openmessage?user_id={wordx[1]}">Игрока</a>')
                    await bot.send_message(wordx[1],
                                           f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a>, передал вам {wordsx[2]} монет\n\n',
                                           parse_mode='HTML')
                    print(wordx[1], wordsx[2])

            except:
                pass
        else:
            try:
                if message.reply_to_message:
                    if message.reply_to_message.from_user.id == message.from_user.id and message.reply_to_message.from_user.id == 2035285317:
                        await message.answer('Вы не можете монеты себе или же боту')
                    else:
                        s = message.text.replace('.', '')

                        word = s.replace('передать -', '').split(" ", 1)
                        s = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
                        connection.commit()
                        wins = s[0]
                        if wins < int(word[1]):
                            await message.answer('Недостаточно монет')
                        else:
                            q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(word[1],
                                                                                                  message.from_user.id))
                            connection.commit()
                            q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(word[1],
                                                                                                  message.reply_to_message.from_user.id))
                            connection.commit()
                            await message.answer(
                                f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a> Передал {sep(word[1], ".")}  монет для <a href="tg://openmessage?user_id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>')
                if not message.reply_to_message:
                    sx = message.text.replace('.', '')
                    wordx = sx.replace('передать', '').split(" ", 2)
                    wordsx = sx.replace('передать', '').split(" ", 3)
                    s = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
                    connection.commit()
                    wins = s[0]
                    if wins < int(wordsx[2]):
                        await message.answer('Недостаточно монет')
                    else:
                        try:
                            if int(wordx[1]) == message.from_user.id:
                                await message.answer("Вы не можете передать себе монеты")
                            else:
                                q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(wordsx[2],
                                                                                                      message.from_user.id))
                                connection.commit()
                                q.execute(
                                    'UPDATE users SET win = win + {} WHERE user_id = {}'.format(wordsx[2], wordx[1]))
                                connection.commit()
                                await message.answer(
                                    f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a> Передал {sep(wordsx[2], ".")}  монет для <a href="tg://openmessage?user_id={wordx[1]}">Игрока</a>')
                                await bot.send_message(wordx[1],
                                                       f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a>, передал вам {wordsx[2]} монет',
                                                       parse_mode='HTML')
                                print(wordx[1])
                        except:
                            await message.answer(" Пользователь не найден")
            except Exception as error:
                await message.answer(f'Ошибка:\n{error}')

    if message.text.lower().startswith('баскетбол'):
        try:
            z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
            connection.commit()
            wins = z[0]
            s = message.text.replace('.', '')
            word = s.replace('баскетбол', '').split(' ', 1)
            if wins < int(word[1]):
                await message.answer('Баланс слишком низкий')
            else:
                dice_mes = await bot.send_dice(message.chat.id, '🏀')
                value = dice_mes.dice.value
                if value in [1, 2, 3]:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1])}'
                    await message.answer(f"Мимо! <b>-{sep(djeks, '.')}</b> Монет. Попробуй еще раз\n")
                    q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()

                if value in [4, 5]:
                    await asyncio.sleep(4)
                    djeks = f'{int(word[1]) * 3}'
                    await message.answer(f"Поздравляю, ты попал прям в сетку! <b>+{sep(djeks, '.')} </b> монет\n")
                    q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                    connection.commit()

        except Exception as error:
            await message.answer(f'Ошибка:\n{error}')

    if message.text.lower() == 'баланс':
        try:
            z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
            connection.commit()
            wins = z[0]
            await message.answer(f'💰 Ваш баланс {sep(round(wins), ".")}')
        except Exception as error:
            await message.answer(f'Ошибка:\n{error}')

    if message.text.lower().startswith('казино'):
        try:
            z = q.execute(f'SELECT win FROM users WHERE user_id = {message.from_user.id}').fetchone()
            connection.commit()
            wins = z[0]
            s = message.text.replace('.', '')
            word = s.replace('казино', '').split(" ", 1)
            if wins < int(word[1]):
                    await message.answer('Баланс слишком низкий')
            else:

                    dice_mes = await bot.send_dice(message.chat.id, '🎰')
                    value = dice_mes.dice.value
                    if value in [54, 26, 24, 62, 44, 2, 60, 61, 9, 59, 52, 49, 39, 63, 32, 23, 56, 4, 35, 27, 17, 21, 2,
                                 16, 13, 5, 47, 5, 33, 30, 41, 38, 3, 48, 42]:
                        await asyncio.sleep(2.3)
                        djeks = f'{int(word[1]) * 2}'
                        await message.answer(f"Пара! <b>+{sep(djeks, '.')}</b> Монет.\n", parse_mode='HTML')
                        q.execute(
                            'UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                        connection.commit()

                    if value in [22, 1, 43]:
                        await asyncio.sleep(2.3)
                        djeks = f'{int(word[1]) * 6}'
                        await message.answer(f"ДЖЕКПОТ!!! <b>+{sep(djeks, '.')}</b> монет.\n", parse_mode='HTML')
                        q.execute(
                            'UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                        connection.commit()

                    if value in [64]:
                        await asyncio.sleep(2.3)
                        djeks = f'{int(word[1]) * 10}'
                        await message.answer(f"МЕГА ДЖЕКПОТ!!! <b>+{sep(djeks, '.')}</b> монет.\n",
                                             parse_mode='HTML')
                        q.execute(
                            'UPDATE users SET win = win + {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                        connection.commit()

                    if value not in [22, 64, 1, 43, 54, 26, 24, 62, 44, 2, 60, 61, 9, 59, 52, 49, 39, 63, 32, 23, 56, 4,
                                     35, 27, 17, 21, 2, 16, 13, 5, 47, 5, 33, 30, 41, 38, 3, 48, 42]:
                        await asyncio.sleep(2.3)
                        djeks = f'{int(word[1])}'
                        await message.answer(
                            f"Ничего не сопало, <b>-{sep(djeks, '.')} </b> монет\nПопробуйте еще раз.\n",
                            parse_mode='HTML')
                        q.execute(
                            'UPDATE users SET win = win - {} WHERE user_id = {}'.format(djeks, message.from_user.id))
                        connection.commit()

        except Exception as error:
            await message.answer(f'Ошибка:\n{error}')


executor.start_polling(dp, skip_updates=True)
#слито в @smoke_software