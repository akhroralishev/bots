import telebot
from telebot import types
import requests
import time

# Token va ID lar
TOKEN = 'botni tokeni'
CHANNEL_ID = 'kanal useri'
ADMIN_GROUP_ID = 'Adminlar guruhi'
bot = telebot.TeleBot(TOKEN)
forwarded_message_map = {}

# Obuna tekshirish
def check_subscription(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get('result', {}).get('status', '')
    return status in ['member', 'administrator', 'creator']

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        bot.send_message(message.chat.id, "Assalomu alaykum! Ismingizni kiriting:")
        bot.register_next_step_handler(message, ask_name)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        markup.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subscribe"))
        bot.send_message(message.chat.id, "Botdan foydalanish uchun avval kanalga obuna bo‘ling.", reply_markup=markup)

# Callback tugmalar
@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    if call.data == 'check_subscribe':
        user_id = call.from_user.id
        if check_subscription(user_id):
            bot.answer_callback_query(call.id, text="✅ Obuna muvaffaqiyatli!", show_alert=True)
            bot.send_message(call.message.chat.id, "Assalomu alaykum! Ismingizni kiriting:")
            bot.register_next_step_handler(call.message, ask_name)
        else:
            bot.answer_callback_query(call.id, text="❌ Hali obuna bo‘lmagansiz!", show_alert=True)

    elif call.data == 'about_center':
        bot.answer_callback_query(call.id)
        with open("docs/qaror.pdf", "rb") as pdf_file:
            bot.send_document(call.message.chat.id, pdf_file, caption="📄 Markaz haqida ma'lumot: Quyidagi faylda markaz faoliyati haqida qaror bilan tanishishingiz mumkin.")
        back_markup = types.InlineKeyboardMarkup()
        back_markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="main_menu"))
        bot.send_message(call.message.chat.id, "⬅️ Asosiy menyuga qaytish uchun 'Orqaga' tugmasini bosing:", reply_markup=back_markup)


    elif call.data == 'about_choices':
        bot.answer_callback_query(call.id)
        tanlovlar_text = (
            "1. Ilhom mukofoti tanlovi\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/1x4YazN4i1LdWOXpfhEZINQ5afPIUovAu/view)\n\n"
            "2. Talabalar teatr studiyalari\n"
            "🔗 [Batafsil](https://docs.google.com/document/d/1Uxbukf91hRfINqHmYcwUysmA6_2xLL5lsa4zv57i60I/edit?tab=t.0)\n\n"
            "3. Ma'rifat maydoni tanlovi\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/1MVuWbed2JwUkG-CoBz_Fv2cn364-6Rio/view)\n\n"
            "4. Munozara\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/1WaHlnEnVBU3ceLuxftijxy8_HRDB9yni/view)\n\n"
            "5. Inson huquqlari\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/15ltvb5GoapB3-cTPsJmfgrBv3uFESYOc/view)\n\n"
            "6. Kitobxon yoshlar ligasi\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/1BKSDSTLmmonH7ZEW2wxjIl2rVvkViccg/view)\n\n"
            "7. Mirzo Ulugʻbek vorislari\n"
            "🔗 [Batafsil](https://lex.uz/docs/-5830270#-5832950)\n\n"
            "8. Islohatlar bilimdoni\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/1lyKyE9cjLIUHC1NLhOD2e-vzl_RLSNRm/view)\n\n"
            "9. Yil talabasi\n"
            "🔗 [Batafsil](https://drive.google.com/file/d/19MTGucXe0W1C-7xeTHnV67hIdnzfY_CA/view)"
        )
        back_markup = types.InlineKeyboardMarkup()
        back_markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="main_menu"))
        bot.edit_message_text(tanlovlar_text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=back_markup)

    elif call.data == 'contact_center':
        bot.answer_callback_query(call.id)
        contact_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        contact_btn.add(types.KeyboardButton("📱 Kontaktni ulashish", request_contact=True))
        contact_btn.add(types.KeyboardButton("🔙 Orqaga"))
        msg = bot.send_message(call.message.chat.id, "📞 Iltimos, kontaktni yuboring yoki 'Orqaga' tugmasini bosing:", reply_markup=contact_btn)
        bot.register_next_step_handler(msg, ask_phone)

    elif call.data == 'main_menu':
        send_main_menu(call.message.chat.id)

# Ism va familiya bosqichlari
def ask_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Familiyangizni kiriting:")
    bot.register_next_step_handler(message, ask_surname, name)

def ask_surname(message, name):
    surname = message.text
    full_name = f"{name} {surname}"
    send_main_menu(message.chat.id, full_name)

# Asosiy menyu
def send_main_menu(chat_id, full_name=None):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📄 Markaz haqida ma'lumot", callback_data='about_center'))
    markup.add(types.InlineKeyboardButton("🏆 Tanlovlar haqida", callback_data='about_choices'))
    markup.add(types.InlineKeyboardButton("📬 Markazga murojat", callback_data='contact_center'))

    welcome_text = f"Rahmat, {full_name}! Endi siz botdan foydalanishingiz mumkin. Quyidagi bo‘limlardan tanlang:" if full_name else "🏠 Asosiy menyu:"
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# Kontaktni qabul qilish
def ask_phone(message):
    if message.text == "🔙 Orqaga":
        bot.send_message(message.chat.id, "🏠 Asosiy menyuga qaytdingiz.", reply_markup=types.ReplyKeyboardRemove())
        send_main_menu(message.chat.id)
        return


    if message.contact and message.contact.phone_number:
        phone_number = message.contact.phone_number
        bot.send_message(message.chat.id, "✍️ Iltimos, murojaatingizni yozing:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, forward_to_admins, phone_number)
    else:
        bot.send_message(message.chat.id, "❌ Iltimos, kontaktni yuboring.")
        contact_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        contact_btn.add(types.KeyboardButton("📱 Kontaktni ulashish", request_contact=True))
        contact_btn.add(types.KeyboardButton("🔙 Orqaga"))
        msg = bot.send_message(message.chat.id, "📞 Kontaktni ulashing:", reply_markup=contact_btn)
        bot.register_next_step_handler(msg, ask_phone)

# Adminlarga yuborish
def forward_to_admins(message, phone_number):
    inquiry = message.text
    user_id = message.chat.id

    admin_text = f"📩 *Yangi murojat!*\n\n📱 Telefon: {phone_number}\n📝 Murojaat: {inquiry}"
    sent = bot.send_message(ADMIN_GROUP_ID, admin_text, parse_mode="Markdown")

    forwarded_message_map[sent.message_id] = user_id
    bot.send_message(user_id, "✅ Murojaatingiz yuborildi. Adminlar tez orada sizga javob berishadi.")

# Admin javobi
@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def handle_admin_reply(message):
    try:
        original_message_id = message.reply_to_message.message_id
        user_id = forwarded_message_map.get(original_message_id)
        if user_id:
            bot.send_message(user_id, f"📥 Admin javobi:\n\n{message.text}")
        else:
            bot.send_message(message.chat.id, "❌ Foydalanuvchining ID sini aniqlab bo‘lmadi.")
    except Exception as e:
        print(f"Admin javobda xatolik: {e}")

# Ishga tushirish
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Xatolik: {e}")
        time.sleep(15)
