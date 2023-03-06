from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
cancel_but: KeyboardButton= KeyboardButton(text='❌ Отмена')
agree_but: KeyboardButton= KeyboardButton(text='✅ Подтвердить')
keyboard_YN: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[agree_but, cancel_but]],
                                    resize_keyboard=True)

main_but1: KeyboardButton = KeyboardButton(text='⚠️ Сообщить')
main_but2: KeyboardButton = KeyboardButton(text='❔ Помощь')
main_but3: KeyboardButton = KeyboardButton(text='🗒️ Актуальные проблемы')
main_but4: KeyboardButton = KeyboardButton(text='🕗 Моя работа')
main_but5: KeyboardButton = KeyboardButton(text='👥 Добавить человека')

help_but1: KeyboardButton = KeyboardButton(text="⬅️ Назад")
help_but2: KeyboardButton = KeyboardButton(text="➡️ Далее")
help_but3: KeyboardButton = KeyboardButton(text="🙋‍♂️ Взяться")

keyboard_first_help: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[help_but3, help_but2], [cancel_but]],
                                    resize_keyboard=True)

keyboard_main_help: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[help_but1 ,help_but3, help_but2], [cancel_but]],
                                    resize_keyboard=True)


keyboard_s1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[main_but1, main_but2]],
                                    resize_keyboard=True)

keyboard_s2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[main_but1, main_but4],[main_but3, main_but2]],
                                    resize_keyboard=True)

keyboard_s3: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[main_but1, main_but5],[main_but3, main_but2]],
                                    resize_keyboard=True)

keyboard_s4: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[main_but1, main_but5],[main_but3, main_but2]],
                                    resize_keyboard=True)

main_keyboards = ['', keyboard_s1, keyboard_s2, keyboard_s3, keyboard_s4]

floor_1: KeyboardButton = KeyboardButton(text='1️⃣ этаж')
floor_2: KeyboardButton = KeyboardButton(text='2️⃣ этаж')
keyboard_floor: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[floor_1, floor_2],[cancel_but]],
                                    resize_keyboard=True)

whom_1: KeyboardButton= KeyboardButton(text = '🖥️ IT специалист') #0
whom_2: KeyboardButton= KeyboardButton(text = '🧹  Уборщик')#1
whom_3: KeyboardButton= KeyboardButton(text = '🛠️ Ремонтный мастер')#2
whom_4: KeyboardButton= KeyboardButton(text = '🔍  Не определен')

whom_5: KeyboardButton= KeyboardButton(text='🧑‍💻 Сотрудник')
whom_6: KeyboardButton= KeyboardButton(text='🙋‍♂️ Работник')



keyboard_whom: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[whom_1, whom_3],
                                                [whom_2, whom_4],
                                                [cancel_but]],
                                    resize_keyboard=True)

keyboard_whom_1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[whom_5, whom_6],
                                                [cancel_but]],
                                    resize_keyboard=True)
keyboard_whom_2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[whom_1, whom_3],
                                                [whom_2, cancel_but]],
                                    resize_keyboard=True)


front_but: InlineKeyboardButton = InlineKeyboardButton(
    text='➡️ Далее',
    callback_data='next_page')

back_but: InlineKeyboardButton = InlineKeyboardButton(
    text='⬅️ Назад',
    callback_data='previous_page')
get_work_but: InlineKeyboardButton = InlineKeyboardButton(
    text='✅',
    callback_data='get_work')

drop_work: InlineKeyboardButton = InlineKeyboardButton(
    text='❌ Отказаться от задания',
    callback_data='drop_work')

complite_work: InlineKeyboardButton = InlineKeyboardButton(
    text='✅ Выполненно',
    callback_data='complite_work')
cancel_work: InlineKeyboardButton = InlineKeyboardButton(
    text='❌ Отказатся',
    callback_data='cansel_work')

inline_my_work: InlineKeyboardMarkup= InlineKeyboardMarkup(
    inline_keyboard=[[complite_work, cancel_work]])

keyboard_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[back_but,get_work_but, front_but]])

keyboard_inline_in_work: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[back_but, front_but]])

keyboard_drop: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[drop_work]])


'''Присвойте уровень важности вашей проблеме:
Просим Вас не преувеличивать, во избежание ошибок'''

help_answers = [f'У вас нет доступа к функциям бота, если вы сотрудник пожалуйства используйте команду /start или обратитесь в поддержку ',
f'Вы, как сотрудник, можете сообщать о проблемах с помощью кнопки:\n⚠️ Сообщить\nОбратите внимание на систему оценки жалобы: \n1-3 - жалоба добавляется в список проблем\n4-6 - уведомление о жалобе получают все пользователи со статусом "Работник"\n7-9 - сообщение направляется администрации\n10 - ваша жалоба будет направленна напрямую директору\n',

f'*⚠️ Сообщить* - функция _подачи жалобы_\n\n'
f'*🗒️ Актуальные проблемы* - раздел в котором вам доступны _актуальный жалобы_, подходящие вам по профилю, или те где специалист _не определен_. Используйсте клавишу ✅ для того, чтобы _взяться за задачу_\n\n'
f'*🕗 Моя работа* - здесь вы можете просмотреть жалобу, за которую взялись. Вы можете отметить ее _выполненной_ или _отказаться_ от нее. Во втором случае жалоба вернется в общий перечень.\n\n'
f'Обратите внимание на систему оценки жалобы: \n'
f'1-3 - жалоба добавляется в список проблем\n'
f'4-6 - уведомление о жалобе получают все пользователи со статусом "Работник"\n'
f'7-9 - сообщение направляется администрации\n10 - ваша жалоба будет направленна напрямую директору\n',

f'У вас есть доступ ко всем актуальным жалобам, вы можете назначать исправление той или иной проблемы на конкретного пользователя',
f'У вас есть полный доступ к quick help\n'
                             'Доступны функции:\n⚠️ Сообщить - используйте при необходимости сообщить о чем-либо\n'
                             '👥 Добавить человека - функция для назначения новых сотрудников/работников/администраторов\n'
                             '🗒️ Актуальные проблемы - список всех актуальных проблем']