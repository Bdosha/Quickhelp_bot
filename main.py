from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from datetime import datetime

import config
import structure
import problems
import data_base
# импорт всех библиотек для работы

BOT_TOKEN: str = config.token


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


#Прописывание всех клавиш

#last_chek: dict = {"last_in_list": 0,
#                   "last_show":{},
#                   "got_work":False,
 #                  "last_id": False}




statuses = [0, 'сотрудник', 'работник', 'администратор', 'директор']

# Функция запуска
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    id = message.from_user.id
    print(message.from_user.username, message.from_user.id)

    got_status = data_base.sql_fetch(id)

    if got_status != -1:   #Пользователь - работник компании
        # далее идет определение класса пользователя и как раз присваивание ему уровня доступа (строка 50)

        await message.answer(f'Ваш статус в системе - {statuses[got_status]}',
                        reply_markup=structure.main_keyboards[got_status])
    else:
        #НН в чате молчать

        data_base.register(id, message.from_user.username)
        got_status = data_base.sql_fetch(id)
        #print(got_status)
        if got_status != -1:     
            await message.answer(f'Ваш статус в системе - {statuses[got_status]}',
                        reply_markup=structure.main_keyboards[got_status])
            return
        await message.answer('У вас нет доступа к функциям бота, если вы сотрудник пожалуйства используйте команду /start или обратитесь в поддержку ', reply_markup=ReplyKeyboardRemove() )




@dp.message(Text(text='❔ Помощь')) # Собственно функция помощи
async def process_help_command(message: Message):
    print(message.from_user.username, message.text)
    #У каждого уровня доступа свой набор функций
    id = message.from_user.id
    got_status = data_base.sql_fetch(id)

    await message.answer(structure.help_answers[got_status], parse_mode= "Markdown")


@dp.message(Text(text='❌ Отмена')) # Функции отмены заполнения жалобы
async def canseling(message: Message):
    print(message.from_user.username, message.text)
     # Эта строка встречается в каждой функции, если пользователь не зарегистрирован, то бот не будет реагировать на его команды
    id = message.from_user.id
    data_base.rereport(id)
    
    if data_base.sql_fetch(id) == -1: return
    
    got_status = data_base.sql_fetch(id)

    await message.answer(text='Отменено',
                         reply_markup=structure.main_keyboards[got_status]) 


@dp.message(Text(text='✅ Подтвердить')) # пока что функция не доделана, сейчас она лишь обнуляет жалобу как и отмена
async def agree(message: Message):
    print(message.from_user.username, message.text)

    id = message.from_user.id
    if data_base.sql_fetch(id) == -1: return

    id = message.from_user.id
    got_status = data_base.sql_fetch(id)
    
    await message.answer(text='Спасибо за обращение\nВскоре проблема будет устранена',
                         reply_markup=structure.main_keyboards[got_status]) 
    curtime = datetime.now()
    #print(curtime.hour)            
    #print(curtime.minute)
    data = {"progress":None,
            "beg_time":f'{str(curtime.hour)}:{str(curtime.minute)}',
            "start_time":[],
            "finish_time":[], 
            "author":f"{id}", 
            "fixer" : data_base.get_from_base(id, 'making_problem', 'fixer'), 
            "loc":data_base.get_from_base(id, 'making_problem','location') + ' ' + data_base.get_from_base(id, 'making_problem','dot'), 
            "message":data_base.get_from_base(id, 'making_problem','message')} 
    
    #print(data)
    if len(data["beg_time"].split(':')[1]) == 1:
        data["beg_time"] = data["beg_time"].split(':')[0] +':0' + data["beg_time"].split(':')[1]
    names= problems.get_names(id)
    problems.new_report(data)
    level = data_base.get_from_base(id, 'making_problem','level')
    if 4 <= level <= 6:
        for i in data_base.get_ids(2):
            if i[0] != message.from_user.id: 
                temp = data_base.get_from_base(id, 'making_problem', 'fixer')
                #print(temp)
                if temp == data_base.get_from_base(i[0], 'user_info', 'work') or temp == -1:
                    times = data["beg_time"].split(':')
                    if len(data["beg_time"].split(':')[1]) == 1:
                        times[1] = data["beg_time"].split(':')[0] +':0' + data["beg_time"].split(':')[1]
                    await bot.send_message(i[0], f'Внимание, поступила жалоба\nУровень важности: {level} \nТребуется: {config.work_list[temp]}\nМесто: {data["loc"]} \nКраское описание: {data["message"]}\n\n@{names[0]} {names[1]}\n{times}') 
    elif 7 <= level <= 9:
        for i in data_base.get_ids(3):
            if i[0] != message.from_user.username:
                await bot.send_message(i[0], f'Внимание, поступила жалоба\nУровень важности: {level} \nТребуется: {config.work_list[temp]}\nМесто: {data["loc"]} \nКраское описание: {data["message"]}\n\n@{names[0]} {names[1]}\n{data["beg_time"]}') 
    elif level == 10:
        for i in data_base.get_ids(4):
            if i != message.from_user.username:
                await bot.send_message(i[0], f'Внимание, поступила жалоба\nУровень важности: {level} \nТребуется: {config.work_list[temp]}\nМесто: {data["loc"]} \nКраское описание: {data["message"]}\n\n@{names[0]} {names[1]}\n{data["beg_time"]}') 
    data_base.rereport(id)


@dp.message(Text(text='⚠️ Сообщить'))
async def report(message: Message):
    print(message.from_user.username, message.text)
    id = message.from_user.id
    #print(data_base.sql_fetch(id))
    if data_base.sql_fetch(id) == -1: return
    await message.answer(text='Чья именно помощь нужна?', # начало ее заполнения
                         reply_markup=structure.keyboard_whom)   #Вызов клавиш выбора персонала

@dp.message(Text(text=['🖥️ IT специалист','🧹  Уборщик','🛠️ Ремонтный мастер','🔍  Не определен'])) # Собственно выбор персонала
async def set_fixer(message: Message):
    print(message.from_user.username, message.text)
    id = message.from_user.id
    if data_base.sql_fetch(id = id) == -1: return

    if data_base.get_from_base(id, 'making_problem', 'new_user') == 'True':
        temp = data_base.get_from_base(id, 'making_problem', 'message').split()
        data_base.new_user(temp[0][1:], f'{temp[1]} {temp[2]}', 2, config.work_list.index(message.text))
        await message.answer(text='Новый работник успешно зарегистрирован в системе', 
                             reply_markup=structure.main_keyboards[data_base.get_from_base(id, 'user_info', 'status')])
        data_base.rereport(id)
        return
    temp = config.work_list.index(message.text)
    if message.text == '🔍  Не определен':
        temp = -1
    data_base.edit_problem(id, 'fixer', temp)  # Заполение ответственного 
    
    await message.answer(text='На какой этаж требуется специалист?',
                         reply_markup=structure.keyboard_floor) #Клавиши выбора этажа
    
@dp.message(Text(text=['1️⃣ этаж', '2️⃣ этаж'])) # Шок контент - выбор этажа
async def set_zone(message: Message):
    print(message.from_user.username, message.text)

    id = message.from_user.id
    if data_base.sql_fetch(id) == -1: return

    data_base.edit_problem(id, 'location', message.text) # запись этажа
    data_base.edit_problem(id, 'dot', "True") 

    await message.answer(text='Укажите точное место возникновения проблемы', 
                         reply_markup=ReplyKeyboardRemove()) # удаление клавиш
    data_base.edit_problem(id, 'new_user', 'NULL')


@dp.message(Text(text=['🧑‍💻 Сотрудник', '🙋‍♂️ Работник'])) # Шок контент - выбор этажа
async def set_new_status(message: Message):
    print(message.from_user.username, message.text)

    id = message.from_user.id
    if data_base.sql_fetch(id) < 3: return

    data_base.edit_problem(id, 'location', ['🧑‍💻 Сотрудник', '🙋‍♂️ Работник'].index(message.text)+1) # запись этажа
    if ['🧑‍💻 Сотрудник', '🙋‍♂️ Работник'].index(message.text)+1 == 1:
        temp = data_base.get_from_base(id, 'making_problem', 'message').split()
        data_base.new_user(temp[0][1:], f'{temp[1]} {temp[2]}', 1)
        await message.answer(text='Сотрудник успешно зарегистрирован в системе', 
                             reply_markup=structure.main_keyboards[data_base.get_from_base(id, 'user_info', 'status')])
        data_base.rereport(id)

        return
    await message.answer(text='Какому профилю соответствует новый работник?', 
                         reply_markup=structure.keyboard_whom_2) # удаление клавиш
    


@dp.message(Text(text='🗒️ Актуальные проблемы'))
async def reports(message: Message):
    print(message.from_user.username, message.text)
    id = message.from_user.id
    if data_base.sql_fetch(id) < 2: return
    
    work_keys = structure.keyboard_inline
    #print(data_base.get_from_base(id, "user_info", 'task'))

    if data_base.get_from_base(id, "user_info", 'task') != None and data_base.get_from_base(id, "user_info", 'task') != 0:
        work_keys=structure.keyboard_inline_in_work
    
    temp = problems.view_report(id)
    if temp[1] == -1:
        await message.answer(text=temp[0])
        return
    #print(temp)
    data_base.edit_task(id, 'text', temp[0])
    data_base.edit_task(id, 'last_check', temp[1])
    #await message.answer(text='Обратите внимание:\nДля того чтоб взяться за задачу - нажмите на "✅"') 
    await message.answer(text=temp[0],reply_markup=work_keys)


@dp.message(Text(text=['🕗 Моя работа'])) # Шок контент - выбор этажа
async def my_work(message: Message):
    print(message.from_user.username, message.text)
    id = message.from_user.id
    if data_base.sql_fetch(id) < 2: return
    #print(data_base.get_from_base(id, 'user_info', 'task'))
    problem = data_base.view_my_work(data_base.get_from_base(id, 'user_info', 'task'))
    #print(problem)
    if problem[1] == None:
        await message.answer(text=problem[0]) 
        return

    await message.answer(text=problem[0],reply_markup=structure.inline_my_work)

@dp.message(Text(text=['👥 Добавить человека'])) # Шок контент - выбор этажа
async def new_user(message: Message):
    print(message.from_user.username, message.text)
    id = message.from_user.id
    if data_base.sql_fetch(id) < 3: return
    data_base.rereport(id)

    await message.answer(text='''Для добавления нового пользователя в базу данных бота требудются следующие данные
    @тег_пользователя Фамилия Имя''', reply_markup=ReplyKeyboardRemove())
    data_base.edit_problem(id, 'new_user', 'True')

@dp.callback_query(Text(text=['next_page']))
async def next_page(callback: CallbackQuery):
    id = callback.from_user.id
    last_check = data_base.get_from_base(id, 'tasks_view', 'last_check')
    temp = problems.next_page(id, last_check)
    data_base.edit_task(id, 'last_check', temp[1])
    #print(last_check)

    #print(temp)
    if temp[1] == None:
        await callback.message.edit_text(text=temp[0])
        return
    #print(textt, last_chek['last_in_list'])
    if callback.message.text != temp[0]:
        await callback.message.edit_text(
            text=temp[0],
            reply_markup=callback.message.reply_markup)

    await callback.answer()

@dp.callback_query(Text(text=['previous_page']))
async def prev_page(callback: CallbackQuery):
    id = callback.from_user.id
    last_check = data_base.get_from_base(id, 'tasks_view', 'last_check')
    temp = problems.prev_page(id, last_check)
    data_base.edit_task(id, 'last_check', temp[1])
    #print(last_check)

    #print(temp)
    if temp[1] == None:
        await callback.message.edit_text(text=temp[0])
        return
    #print(textt, last_chek['last_in_list'])
    if callback.message.text != temp[0]:
        await callback.message.edit_text(
            text=temp[0],
            reply_markup=callback.message.reply_markup)

    await callback.answer()


@dp.callback_query(Text(text=['get_work']))
async def get_work(callback: CallbackQuery):
    id = callback.from_user.id

    temp = problems.get_work(data_base.get_from_base(id, 'tasks_view', 'last_check'))
    if temp == -1:
        await callback.message.edit_text(
            text=temp[0])
        data_base.edit_task(id, 'last_check', 0)
        data_base.edit_base(id, 'user_info', 'task', temp[1])

    else:
        await callback.message.edit_text(
            text=callback.message.text + "\n✅ Задание доступно в разделе Моя работа")
        data_base.edit_base(id, 'user_info', 'task', temp)
    #data_base.edit_task(id, 'last_check', 0)

@dp.callback_query(Text(text=['complite_work']))
async def complite_work(callback: CallbackQuery):
    id = callback.from_user.id
    problem = data_base.get_from_base(id, 'user_info', 'task')
    data_base.complite_work(id, problem)
    await callback.message.edit_text(text="Проблема отмечена исправленной! \nСпасибо за помощь")

@dp.callback_query(Text(text=['cansel_work']))
async def cansel_work(callback: CallbackQuery):
    id = callback.from_user.id
    problem = data_base.get_from_base(id, 'user_info', 'task')
    data_base.cansel_work(id, problem)
    await callback.message.edit_text(text="Вы отказались от задания, жалоба возвращена в общий доступ")


@dp.message()
async def text_message(message: Message): # эта функция записывает в жалобу те данные, которые нельзя ввести с кнопок,
    # вроде точного местоположения и характеристики проблемы
    print(message.from_user.username, message.text)
    id = message.from_user.id
    #print(data_base.get_from_base(id, 'making_problem', 'dot'))
    if message.text == '18362':
        try:
            data_base.new_user(message.from_user.username, 'Жюри Жюри', 2, 0)
            data_base.register(message.from_user.id, message.from_user.username)
            await message.answer(f'Регистрация прошла успешна, вам присвоем статус: работник',
                        reply_markup=structure.main_keyboards[2])
        except:
            await message.answer(f'Произошла ошибка, возможно вы уже зарегистрированы')




    elif data_base.get_from_base(id, 'making_problem', 'dot') == "True":
        data_base.edit_problem(id, 'dot', message.text) 

        await message.answer(text='Постарайтесь кратко и ёмко обозначить проблему ')
        data_base.edit_problem(id, 'message', "True")
            
    elif data_base.get_from_base(id, 'making_problem', 'message') == "True":

        data_base.edit_problem(id, 'message', message.text)
        data_base.edit_problem(id, 'level', "True")

        await message.answer(text="Присвойте своей жалобе уровень важности от 1 до 10\nДля корректной оценки рекомендуем обратиться к пункту ❔ Помощь")
    elif data_base.get_from_base(id, 'making_problem', 'new_user') == "True":
        try:
            message.text.split(3)
            data_base.edit_problem(id, 'message', message.text)
            await message.answer(text="Присвойте новому пользователю уровень в системе бота", reply_markup=structure.keyboard_whom_1)
        except:
            await message.answer(text="Некоректный ввод данных")
        


    elif data_base.get_from_base(id, 'making_problem', 'level') == "True":
        try:
            if 1 <= int(message.text) <= 10:
                data_base.edit_problem(id, 'level', int(message.text))
                await message.answer(text=f"Требуется {config.work_list[ data_base.get_from_base(id, 'making_problem', 'fixer')]}\n"
                                f"Место: {data_base.get_from_base(id, 'making_problem', 'location')}, {data_base.get_from_base(id, 'making_problem', 'dot')}\n"
                                f"Краткое описание: {data_base.get_from_base(id, 'making_problem', 'message')}\n\n"
                                f'Подтвердить отправку сообщения?',
                            reply_markup=structure.keyboard_YN)

            else:
                await message.answer(text="Пожалуйста введите число в диапозоне от 1 до 10")
        except:
            await message.answer(text="Пожалуйста введите число в диапозоне от 1 до 10")
    else:
        tex = message.text.split('\n')[0]
        await message.answer(text = f'Неизвестная команда', reply_markup=structure.main_keyboards[data_base.get_from_base(id, 'user_info', 'status')])

if __name__ == '__main__':
    dp.run_polling(bot) # Запуск бота