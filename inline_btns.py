from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

course_btns = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='1', callback_data='1'),
    InlineKeyboardButton(text='2', callback_data='2'),
    InlineKeyboardButton(text='3', callback_data='3'),
    InlineKeyboardButton(text='4', callback_data='4'),
    InlineKeyboardButton(text='5', callback_data='5')
]])

first_btns = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1.1', callback_data='11'),
        InlineKeyboardButton(text='1.2', callback_data='12')
    ],
    [
        InlineKeyboardButton(text='2.1', callback_data='21')
    ],
    [
        InlineKeyboardButton(text='3.1', callback_data='31'),
        InlineKeyboardButton(text='3.2', callback_data='32'),
        InlineKeyboardButton(text='3.3', callback_data='33')
    ],
    [
        InlineKeyboardButton(text='4.1', callback_data='41')
    ],
    [
        InlineKeyboardButton(text='5.1', callback_data='51'),
        InlineKeyboardButton(text='5.2', callback_data='52')
    ]
])

second_btns = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1.1', callback_data='11'),
        InlineKeyboardButton(text='1.2', callback_data='12')
    ],
    [
        InlineKeyboardButton(text='2.1', callback_data='21')
    ],
    [
        InlineKeyboardButton(text='3.1', callback_data='31'),
        InlineKeyboardButton(text='3.2', callback_data='32'),
        InlineKeyboardButton(text='3.3', callback_data='33')
    ],
    [
        InlineKeyboardButton(text='4.1', callback_data='41'),
        InlineKeyboardButton(text='4.2', callback_data='42')
    ],
    [
        InlineKeyboardButton(text='5.1', callback_data='51'),
        InlineKeyboardButton(text='5.2', callback_data='52')
    ]
])

third_btns = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='КАТМА', callback_data='11'),
        InlineKeyboardButton(text='КУЧП', callback_data='12')
    ],
    [
        InlineKeyboardButton(text='КММ', callback_data='21')
    ],
    [
        InlineKeyboardButton(text='КМА ММЭ (3.1)', callback_data='31'),
        InlineKeyboardButton(text='КМА ММЭ (3.2)', callback_data='32'),
        InlineKeyboardButton(text='КФА', callback_data='33')
    ],
    [
        InlineKeyboardButton(text='КТФ', callback_data='41'),
        InlineKeyboardButton(text='КМА МАиП', callback_data='42')
    ]
])

fourth_btns = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='КАТМА', callback_data='11'),
        InlineKeyboardButton(text='КУЧП', callback_data='12')
    ],
    [
        InlineKeyboardButton(text='КММ', callback_data='21')
    ],
    [
        InlineKeyboardButton(text='КМА ММЭ', callback_data='31'),
        InlineKeyboardButton(text='КМА МАиП', callback_data='42'),
        InlineKeyboardButton(text='КФА', callback_data='33')
    ],
    [
        InlineKeyboardButton(text='КТФ', callback_data='41')
    ]
])

fifth_btns = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='КТФ', callback_data='41'),
        InlineKeyboardButton(text='КМА МАиП', callback_data='42')
    ]
])
