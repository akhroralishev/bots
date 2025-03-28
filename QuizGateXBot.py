from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes

TOKEN = "IP Token "
CHANNEL_USERNAME = "botni admin qilgan telegram kanal usernamesini kiriting"  # Obuna boʻlishi kerak boʻlgan kanal

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print("user_id: ",user_id)
    print("update: ",update)
    try:
        
        # Obunani tekshirish
        print("Obuna tekshirishga kirildi")
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        print("context: ",context.args)
        
        print("member val: ",member)
        if member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text("Viktorinani boshlash uchun /quiz ni bosing!")
        else:
            # Obuna boʻlmagan foydalanuvchiga xabar
            keyboard = [
                [InlineKeyboardButton("Kanalga Obuna Bo‘lish", url=f"https://@")],
                [InlineKeyboardButton("Tekshirish", callback_data="check_sub")]
            ]

            await update.message.reply_text(
                "Javob berish uchun kanalga obuna boʻling!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except Exception as e:
        print(e)
        await update.message.reply_text("Xatolik yuz berdi. Iltimos, qayta urinib koʻring.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check_sub":
        # Qayta tekshirish
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=query.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text("Obuna tasdiqlandi! Viktorinani boshlash uchun /quiz ni bosing.")
        else:
            await query.edit_message_text("Siz hali obuna boʻlmadingiz. Iltimos, kanalga obuna boʻling.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Viktorinani boshlash
    await update.message.reply_poll(
        question="Savol matni",
        options=["A", "B", "C", "D"],
        correct_option_id=0,
        is_anonymous=False
    )

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot ishga tushdi...")
    app.run_polling()
