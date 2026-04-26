import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# ============ SOZLAMALAR ============
TOKEN = "8652719743:AAEvLMvUXi3-RKgkLhJIEHKKin9BOY4j0jE"
BOOKING_URL = "https://www.booking.com/index.html?aid=304142"
AVIASALES_URL = "https://www.aviasales.uz/?params=TAS1"
ADMIN_CONTACT = "@khamidov_0616"

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

TEXTS = {
    'uz': {
        'welcome': "✈️ *The One Voyage* ga xush kelibsiz!\n\nBiz sizga eng yaxshi sayohat tajribasini taqdim etamiz.\n\nQuyidagi bo'limlardan birini tanlang 👇",
        'hotel': "🏨 Mehmonxona",
        'transfer': "🚗 Transfer",
        'price': "💰 Narxlar",
        'package': "📦 Tur paket",
        'contact': "📞 Bog'lanish",
        'back': "⬅️ Orqaga",
        'language': "🌐 Til / Язык",
        'booking_btn': "🏨 Booking.com da qidirish",
        'flights_btn': "✈️ Aviabilet qidirish",
        'package_msg': f"📦 *Tur paket*\n\nTur paketlar haqida ma'lumot olish uchun admin bilan bog'laning:\n\n👤 {ADMIN_CONTACT}\n🕐 10:00 - 22:00",
        'contact_msg': f"📞 *Bog'lanish*\n\n👤 Admin: {ADMIN_CONTACT}\n🕐 Ish vaqti: 10:00 - 22:00\n\nHar qanday savol bo'lsa yozing! 😊",
        'hotel_msg': "🏨 *Mehmonxona qidirish*\n\n1️⃣ Booking.com da o'zingiz qidiring 👇\n2️⃣ Yoki admin ga yozing:\n\n📍 Shahar, 📅 Sana, 👥 Mehmonlar soni\n\n_Misol: Dubay, 10-15 iyun, 2 kishi_",
        'transfer_msg': "🚗 *Transfer qidirish*\n\nQuyidagilarni yozing:\n\n📍 Qayerdan → Qayerga\n📅 Sana va vaqt\n👥 Yo'lovchilar soni\n\n_Misol: Dubay aeroporti → Atlantis, 10-iyun 14:00, 2 kishi_",
        'flights_msg': f"✈️ *Aviabilet qidirish*\n\n1️⃣ Aviasales da o'zingiz qidiring 👇\n2️⃣ Yoki admin orqali: {ADMIN_CONTACT}",
        'request_sent': f"✅ *So'rovingiz qabul qilindi!*\n\nAdmin tez orada bog'lanadi.\n\n📞 {ADMIN_CONTACT}",
        'prices_title': "💰 *Joriy narxlar:*\n\n",
        'prices_footer': f"\n\n📞 Bron: {ADMIN_CONTACT}",
    },
    'ru': {
        'welcome': "✈️ Добро пожаловать в *The One Voyage*!\n\nМы предоставляем лучший опыт путешествий.\n\nВыберите один из разделов 👇",
        'hotel': "🏨 Отель",
        'transfer': "🚗 Трансфер",
        'price': "💰 Цены",
        'package': "📦 Тур пакет",
        'contact': "📞 Связаться",
        'back': "⬅️ Назад",
        'language': "🌐 Til / Язык",
        'booking_btn': "🏨 Найти на Booking.com",
        'flights_btn': "✈️ Найти авиабилет",
        'package_msg': f"📦 *Тур пакет*\n\nДля информации о тур пакетах свяжитесь с администратором:\n\n👤 {ADMIN_CONTACT}\n🕐 10:00 - 22:00",
        'contact_msg': f"📞 *Связаться*\n\n👤 Админ: {ADMIN_CONTACT}\n🕐 Рабочие часы: 10:00 - 22:00\n\nПишите, если есть вопросы! 😊",
        'hotel_msg': "🏨 *Поиск отеля*\n\n1️⃣ Найдите сами на Booking.com 👇\n2️⃣ Или напишите админу:\n\n📍 Город, 📅 Даты, 👥 Гости\n\n_Пример: Дубай, 10-15 июня, 2 человека_",
        'transfer_msg': "🚗 *Поиск трансфера*\n\nНапишите:\n\n📍 Откуда → Куда\n📅 Дата и время\n👥 Пассажиры\n\n_Пример: Аэропорт Дубай → Atlantis, 10 июня 14:00, 2 чел._",
        'flights_msg': f"✈️ *Поиск авиабилетов*\n\n1️⃣ Найдите сами на Aviasales 👇\n2️⃣ Или через админа: {ADMIN_CONTACT}",
        'request_sent': f"✅ *Ваш запрос принят!*\n\nАдминистратор свяжется с вами.\n\n📞 {ADMIN_CONTACT}",
        'prices_title': "💰 *Актуальные цены:*\n\n",
        'prices_footer': f"\n\n📞 Бронирование: {ADMIN_CONTACT}",
    }
}

user_lang = {}
user_state = {}

def get_lang(uid): return user_lang.get(uid, 'uz')
def t(uid, key):
    lang = get_lang(uid)
    return TEXTS[lang].get(key, TEXTS['uz'].get(key, ''))

def main_keyboard(uid):
    T = TEXTS[get_lang(uid)]
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
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(uid, 'back'), callback_data='menu')]])

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
    await update.message.reply_text(t(uid, 'welcome'), parse_mode='Markdown', reply_markup=main_keyboard(uid))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    handlers = {
        'menu': lambda: (setattr(user_state, uid, 'general') or True, t(uid, 'welcome'), main_keyboard(uid)),
    }

    if data == 'menu':
        user_state[uid] = 'general'
        await query.edit_message_text(t(uid, 'welcome'), parse_mode='Markdown', reply_markup=main_keyboard(uid))
    elif data == 'language':
        await query.edit_message_text("🌐 Tilni tanlang / Выберите язык:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
             InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')]
        ]))
    elif data == 'lang_uz':
        user_lang[uid] = 'uz'
        await query.edit_message_text("✅ Til o'zgartirildi!\n\n" + TEXTS['uz']['welcome'], parse_mode='Markdown', reply_markup=main_keyboard(uid))
    elif data == 'lang_ru':
        user_lang[uid] = 'ru'
        await query.edit_message_text("✅ Язык изменён!\n\n" + TEXTS['ru']['welcome'], parse_mode='Markdown', reply_markup=main_keyboard(uid))
    elif data == 'hotel':
        user_state[uid] = 'hotel'
        await query.edit_message_text(t(uid, 'hotel_msg'), parse_mode='Markdown', reply_markup=hotel_keyboard(uid))
    elif data == 'flights':
        user_state[uid] = 'flights'
        await query.edit_message_text(t(uid, 'flights_msg'), parse_mode='Markdown', reply_markup=flights_keyboard(uid))
    elif data == 'transfer':
        user_state[uid] = 'transfer'
        await query.edit_message_text(t(uid, 'transfer_msg'), parse_mode='Markdown', reply_markup=back_keyboard(uid))
    elif data == 'price':
        text = t(uid, 'prices_title')
        for p in PRICES:
            text += f"🔹 *{p['nomi']}*\n   💵 {p['narx']}\n   _{p['izoh']}_\n\n"
        text += t(uid, 'prices_footer')
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=back_keyboard(uid))
    elif data == 'package':
        await query.edit_message_text(t(uid, 'package_msg'), parse_mode='Markdown', reply_markup=back_keyboard(uid))
    elif data == 'contact':
        await query.edit_message_text(t(uid, 'contact_msg'), parse_mode='Markdown', reply_markup=back_keyboard(uid))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = 'general'
    await update.message.reply_text(t(uid, 'request_sent'), parse_mode='Markdown', reply_markup=main_keyboard(uid))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ The One Voyage Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
