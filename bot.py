import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# ============ SOZLAMALAR ============
TOKEN = "8652719743:AAEvLMvUXi3-RKgkLhJIEHKKin9BOY4j0jE"
ADMIN_USERNAME = "@khamidov_0616"
BOOKING_URL = "https://www.booking.com/index.html?aid=304142"
AVIASALES_URL = "https://www.aviasales.uz/?params=TAS1"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ============ NARXLAR ============
PRICES = [
    {"nomi": "🇹🇷 Turkiya - Antaliya", "narx": "$450/kishi", "izoh": "7 kecha, All Inclusive, aviabilet bilan"},
    {"nomi": "🇦🇪 Dubay", "narx": "$680/kishi", "izoh": "5 kecha, Nonushta, aviabilet bilan"},
    {"nomi": "🇪🇬 Misr - Sharm el-Shayx", "narx": "$520/kishi", "izoh": "6 kecha, All Inclusive, aviabilet bilan"},
    {"nomi": "🇹🇭 Tailand - Phuket", "narx": "$750/kishi", "izoh": "7 kecha, Nonushta, aviabilet bilan"},
    {"nomi": "🇮🇹 Italiya - Rim", "narx": "$1100/kishi", "izoh": "5 kecha, B&B, aviabilet bilan"},
    {"nomi": "🚗 Transfer - Dubay aeroporti", "narx": "$25/yo'lovchi", "izoh": "Aeroportdan mehmonxonagacha"},
    {"nomi": "🚗 Transfer - Antaliya aeroporti", "narx": "$15/yo'lovchi", "izoh": "Aeroportdan mehmonxonagacha"},
]

# ============ TILLAR ============
TEXTS = {
    'uz': {
        'welcome': (
            "✈️ *The One Voyage* ga xush kelibsiz!\n\n"
            "Biz sizga eng yaxshi sayohat tajribasini taqdim etamiz.\n\n"
            "Quyidagi bo'limlardan birini tanlang 👇"
        ),
        'hotel': "🏨 Mehmonxona",
        'transfer': "🚗 Transfer",
        'price': "💰 Narxlar",
        'package': "📦 Tur paket",
        'contact': "📞 Bog'lanish",
        'back': "⬅️ Orqaga",
        'language': "🌐 Til / Язык",
        'booking_btn': "🏨 Booking.com da qidirish",
        'flights_btn': "✈️ Aviabilet qidirish",
        'package_msg': (
            "📦 *Tur paket*\n\n"
            "Tur paketlar haqida batafsil ma'lumot olish uchun "
            "admin bilan bog'laning:\n\n"
            f"👤 Admin: {ADMIN_USERNAME}\n"
            "🕐 Ish vaqti: 10:00 - 22:00\n\n"
            "Admin siz bilan tez orada bog'lanadi! ✅"
        ),
        'contact_msg': (
            "📞 *Bog'lanish*\n\n"
            f"👤 Admin: {ADMIN_USERNAME}\n"
            "🕐 Ish vaqti: 10:00 - 22:00\n\n"
            "Har qanday savol bo'lsa bemalol yozing! 😊"
        ),
        'hotel_msg': (
            "🏨 *Mehmonxona qidirish*\n\n"
            "2 ta usul mavjud:\n\n"
            "1️⃣ *Booking.com* da o'zingiz qidiring 👇\n"
            "2️⃣ Yoki quyida ma'lumot yuboring, admin yordam beradi:\n\n"
            "📍 Shahar / Mamlakat\n"
            "📅 Kirish sanasi\n"
            "📅 Chiqish sanasi\n"
            "👥 Mehmonlar soni\n"
            "⭐ Yulduz (ixtiyoriy)\n\n"
            "_Misol: Dubay, 10-iyun, 15-iyun, 2 kishi, 5 yulduz_"
        ),
        'transfer_msg': (
            "🚗 *Transfer qidirish*\n\n"
            "Quyidagi ma'lumotlarni yuboring:\n\n"
            "📍 Qayerdan\n"
            "📍 Qayerga\n"
            "📅 Sana va vaqt\n"
            "👥 Yo'lovchilar soni\n\n"
            "_Misol: Dubay aeroporti → Atlantis Hotel, 10-iyun 14:00, 2 kishi_"
        ),
        'flights_msg': (
            "✈️ *Aviabilet qidirish*\n\n"
            "2 ta usul:\n\n"
            "1️⃣ *Aviasales* da o'zingiz qidiring 👇\n"
            "2️⃣ Yoki admin orqali bron qiling:\n\n"
            f"👤 {ADMIN_USERNAME}"
        ),
        'request_sent': (
            "✅ *So'rovingiz qabul qilindi!*\n\n"
            "Admin tez orada siz bilan bog'lanadi.\n\n"
            f"📞 O'zingiz ham yozishingiz mumkin: {ADMIN_USERNAME}"
        ),
        'prices_title': "💰 *Joriy narxlar:*\n\n",
        'prices_footer': f"\n\n📞 Bron qilish: {ADMIN_USERNAME}",
    },
    'ru': {
        'welcome': (
            "✈️ Добро пожаловать в *The One Voyage*!\n\n"
            "Мы предоставляем лучший опыт путешествий.\n\n"
            "Выберите один из разделов 👇"
        ),
        'hotel': "🏨 Отель",
        'transfer': "🚗 Трансфер",
        'price': "💰 Цены",
        'package': "📦 Тур пакет",
        'contact': "📞 Связаться",
        'back': "⬅️ Назад",
        'language': "🌐 Til / Язык",
        'booking_btn': "🏨 Найти на Booking.com",
        'flights_btn': "✈️ Найти авиабилет",
        'package_msg': (
            "📦 *Тур пакет*\n\n"
            "Для получения подробной информации о тур пакетах "
            "свяжитесь с администратором:\n\n"
            f"👤 Админ: {ADMIN_USERNAME}\n"
            "🕐 Рабочие часы: 10:00 - 22:00\n\n"
            "Администратор свяжется с вами в ближайшее время! ✅"
        ),
        'contact_msg': (
            "📞 *Связаться*\n\n"
            f"👤 Админ: {ADMIN_USERNAME}\n"
            "🕐 Рабочие часы: 10:00 - 22:00\n\n"
            "Пишите, если есть вопросы! 😊"
        ),
        'hotel_msg': (
            "🏨 *Поиск отеля*\n\n"
            "2 способа:\n\n"
            "1️⃣ Найдите сами на *Booking.com* 👇\n"
            "2️⃣ Или отправьте данные, админ поможет:\n\n"
            "📍 Город / Страна\n"
            "📅 Дата заезда\n"
            "📅 Дата выезда\n"
            "👥 Количество гостей\n"
            "⭐ Звёздность (по желанию)\n\n"
            "_Пример: Дубай, 10 июня, 15 июня, 2 человека, 5 звёзд_"
        ),
        'transfer_msg': (
            "🚗 *Поиск трансфера*\n\n"
            "Отправьте следующую информацию:\n\n"
            "📍 Откуда\n"
            "📍 Куда\n"
            "📅 Дата и время\n"
            "👥 Количество пассажиров\n\n"
            "_Пример: Аэропорт Дубай → Atlantis Hotel, 10 июня 14:00, 2 человека_"
        ),
        'flights_msg': (
            "✈️ *Поиск авиабилетов*\n\n"
            "2 способа:\n\n"
            "1️⃣ Найдите сами на *Aviasales* 👇\n"
            "2️⃣ Или закажите через админа:\n\n"
            f"👤 {ADMIN_USERNAME}"
        ),
        'request_sent': (
            "✅ *Ваш запрос принят!*\n\n"
            "Администратор свяжется с вами в ближайшее время.\n\n"
            f"📞 Можете написать сами: {ADMIN_USERNAME}"
        ),
        'prices_title': "💰 *Актуальные цены:*\n\n",
        'prices_footer': f"\n\n📞 Бронирование: {ADMIN_USERNAME}",
    }
}

user_lang = {}
user_state = {}

def get_lang(uid):
    return user_lang.get(uid, 'uz')

def t(uid, key):
    lang = get_lang(uid)
    return TEXTS[lang].get(key, TEXTS['uz'].get(key, ''))

def main_keyboard(uid):
    lang = get_lang(uid)
    T = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(T['hotel'], callback_data='hotel'),
         InlineKeyboardButton(T['transfer'], callback_data='transfer')],
        [InlineKeyboardButton(T['flights_btn'], callback_data='flights'),
         InlineKeyboardButton(T['price'], callback_data='price')],
        [InlineKeyboardButton(T['package'], callback_data='package'),
         InlineKeyboardButton(T['contact'], callback_data='contact')],
        [InlineKeyboardButton(T['language'], callback_data='language')],
    ])

def back_keyboard(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(uid, 'back'), callback_data='menu')]
    ])

def hotel_keyboard(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(uid, 'booking_btn'), url=BOOKING_URL)],
        [InlineKeyboardButton(t(uid, 'back'), callback_data='menu')]
    ])

def flights_keyboard(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(uid, 'flights_btn'), url=AVIASALES_URL)],
        [InlineKeyboardButton(t(uid, 'back'), callback_data='menu')]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        t(uid, 'welcome'),
        parse_mode='Markdown',
        reply_markup=main_keyboard(uid)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    if data == 'menu':
        user_state[uid] = 'general'
        await query.edit_message_text(
            t(uid, 'welcome'),
            parse_mode='Markdown',
            reply_markup=main_keyboard(uid)
        )
    elif data == 'language':
        await query.edit_message_text(
            "🌐 Tilni tanlang / Выберите язык:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
                 InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')]
            ])
        )
    elif data == 'lang_uz':
        user_lang[uid] = 'uz'
        await query.edit_message_text(
            "✅ Til o'zgartirildi!\n\n" + TEXTS['uz']['welcome'],
            parse_mode='Markdown',
            reply_markup=main_keyboard(uid)
        )
    elif data == 'lang_ru':
        user_lang[uid] = 'ru'
        await query.edit_message_text(
            "✅ Язык изменён!\n\n" + TEXTS['ru']['welcome'],
            parse_mode='Markdown',
            reply_markup=main_keyboard(uid)
        )
    elif data == 'hotel':
        user_state[uid] = 'hotel'
        await query.edit_message_text(
            t(uid, 'hotel_msg'),
            parse_mode='Markdown',
            reply_markup=hotel_keyboard(uid)
        )
    elif data == 'flights':
        user_state[uid] = 'flights'
        await query.edit_message_text(
            t(uid, 'flights_msg'),
            parse_mode='Markdown',
            reply_markup=flights_keyboard(uid)
        )
    elif data == 'transfer':
        user_state[uid] = 'transfer'
        await query.edit_message_text(
            t(uid, 'transfer_msg'),
            parse_mode='Markdown',
            reply_markup=back_keyboard(uid)
        )
    elif data == 'price':
        text = t(uid, 'prices_title')
        for p in PRICES:
            text += f"🔹 *{p['nomi']}*\n"
            text += f"   💵 {p['narx']}\n"
            if p.get('izoh'):
                text += f"   _{p['izoh']}_\n"
            text += "\n"
        text += t(uid, 'prices_footer')
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=back_keyboard(uid)
        )
    elif data == 'package':
        await query.edit_message_text(
            t(uid, 'package_msg'),
            parse_mode='Markdown',
            reply_markup=back_keyboard(uid)
        )
    elif data == 'contact':
        await query.edit_message_text(
            t(uid, 'contact_msg'),
            parse_mode='Markdown',
            reply_markup=back_keyboard(uid)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = update.effective_user
    text = update.message.text
    state = user_state.get(uid, 'general')

    state_label = {
        'hotel': '🏨 Mehmonxona',
        'transfer': '🚗 Transfer',
        'flights': '✈️ Aviabilet',
        'general': '💬 Umumiy'
    }.get(state, '💬 Umumiy')

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    admin_msg = (
        f"📩 *Yangi so'rov!*\n"
        f"🕐 {now}\n\n"
        f"👤 Ism: {user.first_name} {user.last_name or ''}\n"
        f"🆔 Username: @{user.username or 'yoq'}\n"
        f"📱 ID: `{uid}`\n"
        f"📂 Bo'lim: {state_label}\n\n"
        f"💬 Xabar:\n{text}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_USERNAME,
            text=admin_msg,
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Admin ga yuborishda xato: {e}")

    user_state[uid] = 'general'
    await update.message.reply_text(
        t(uid, 'request_sent'),
        parse_mode='Markdown',
        reply_markup=main_keyboard(uid)
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ The One Voyage Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
