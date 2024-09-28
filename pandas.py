from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Adminning chat ID'sini aniqlang
ADMIN_CHAT_ID = '7168606778'
TOKEN = '7154776514:AAEAx_ETi8FRJ4NuClB2qYFoMej3GJ1fggY'

# Boshlang'ich menyuni yaratish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("📚 Kurslar")],
        [KeyboardButton("📍 Manzil"), KeyboardButton("📞 Bog'lanish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Assalomu alaykum, PANDA Education Campus botiga xush kelibsiz!", reply_markup=reply_markup)
    context.user_data.clear()  # Foydalanuvchi ma'lumotlarini tozalaymiz

# Kurslar ro'yxatini chiqarish
async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("💻 Kompyuter Savodxonligi"), KeyboardButton("🌐 Web Dasturlash Foundation")],
        [KeyboardButton("💻 Web Dasturlash Frontend"), KeyboardButton("🔧 Web Dasturlash Backend")],
        [KeyboardButton("🎨 Grafik Dizayn"), KeyboardButton("📱 IOS & Android Dasturlash")],
        [KeyboardButton("🏗️ 3DS Max & Autocad"), KeyboardButton("🚛 Logistika")],
        [KeyboardButton("🔙 Ortga qaytish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Quyidagi kurslardan birini tanlang:", reply_markup=reply_markup)

# Kurslar haqida ma'lumot chiqish
async def course_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    selected_course = update.message.text
    context.user_data['selected_course'] = selected_course  # Tanlangan kursni saqlaymiz

    course_data = {
        "💻 Kompyuter Savodxonligi": "Kompyuter Savodxonligi: 1-3 oy\n🎓 Òrgatiladi: Word, Excel, PowerPoint\n💰 Narxi: 200,000 so‘m",
        "🌐 Web Dasturlash Foundation": "Web Dasturlash (Foundation): 3 oy\n🎓 Òrgatiladi: HTML, CSS, JavaScript\n💰 Narxi: 499,000 so‘m",
        "💻 Web Dasturlash Frontend": "Web Dasturlash (Frontend): 6 oy\n🎓 Òrgatiladi: JavaScript, React.js, Vue.js\n💰 Narxi: 499,000 so‘m",
        "🔧 Web Dasturlash Backend": "Web Dasturlash (Backend): 6 oy\n🎓 Òrgatiladi: Python, Django\n💰 Narxi: 499,000 so‘m",
        "🎨 Grafik Dizayn": "Grafik Dizayn: 6 oy\n🎓 Òrgatiladi: Adobe Photoshop, Illustrator\n💰 Narxi: 499,000 so‘m",
        "📱 IOS & Android Dasturlash": "IOS & Android: 9 oy\n🎓 Òrgatiladi: Dart, Flutter\n💰 Narxi: 499,000 so‘m",
        "🏗️ 3DS Max & Autocad": "3DS Max & Autocad: 9 oy\n🎓 Òrgatiladi: 3DS Max, AutoCAD\n💰 Narxi: 499,000 so‘m",
        "🚛 Logistika": "Logistika: 2 oy\n🎓 Òrgatiladi: AQSH Logistikasi\n💰 Narxi: 300$"
    }

    # Tanlangan kurs haqida ma'lumot chiqarish
    course_info_text = course_data.get(selected_course, "Kurs haqida ma'lumot topilmadi.")
    keyboard = [[KeyboardButton("📝 Yozilish")], [KeyboardButton("🔙 Ortga qaytish")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(course_info_text, reply_markup=reply_markup)

# F.I.SH ni kiritishni so'rash
async def ask_for_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Yozilish uchun: F.I.SH ni kiriting:")
    context.user_data['awaiting_name'] = True  # F.I.SH ni kutishni belgilaymiz

# F.I.SH ni qabul qilish va saqlash
async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.text
    context.user_data['name'] = user_name  # F.I.SH ni saqlaymiz
    context.user_data['awaiting_name'] = False  # F.I.SH kutishni to'xtatamiz

    # Kontakt ulashish tugmasini ko'rsatamiz
    keyboard = [[KeyboardButton("📞 Kontakt ulashish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Iltimos, telefon raqamingizni ulashing:",
        reply_markup=reply_markup
    )

# Kontaktni qabul qilish va saqlash
async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.message.contact.phone_number
    context.user_data['contact'] = contact  # Kontaktni saqlaymiz

    # Jo'natish tugmasini ko'rsatamiz
    keyboard = [[KeyboardButton("📤 Jo'natish")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Kontakt qabul qilindi. Ma'lumotlaringizni jo'natish uchun 'Jo'natish' tugmasini bosing.",
        reply_markup=reply_markup
    )

# Ma'lumotlarni adminga jo'natish
async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = context.user_data.get('name', 'Noma\'lum F.I.SH')
    contact = context.user_data.get('contact', 'Noma\'lum kontakt')
    selected_course = context.user_data.get('selected_course', 'Noma\'lum kurs')

    # Adminga ma'lumot yuborish
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Yozilish: {user_name}\nKurs: {selected_course}\nTelefon: {contact}"
    )

    # Foydalanuvchiga muvaffaqiyatli yozilganligini bildirish
    await update.message.reply_text("Yozilish muvaffaqiyatli amalga oshirildi! ✅")

    # Botni boshlang'ich holatga qaytarish
    await start(update, context)

# Manzil haqida ma'lumot berish
async def location_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📍 PANDA Education Campus manzili:\nAsaka shaxar, Soxil bo'yi ko'chasi, 8 uy.")

# Bog'lanish haqida ma'lumot berish
async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📞 Biz bilan bog'lanish uchun:\n+998 77 114 89 88")

# Barcha matnli xabarlarni boshqarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    # Agar F.I.SH ni kutayotgan bo'lsak
    if context.user_data.get('awaiting_name'):
        await receive_name(update, context)
        return

    # Tugmalarni boshqarish
    if text == "📚 Kurslar":
        await courses(update, context)
    elif text in ["💻 Kompyuter Savodxonligi", "🌐 Web Dasturlash Foundation", "💻 Web Dasturlash Frontend", "🔧 Web Dasturlash Backend", "🎨 Grafik Dizayn", "📱 IOS & Android Dasturlash", "🏗️ 3DS Max & Autocad", "🚛 Logistika"]:
        await course_info(update, context)
    elif text == "📝 Yozilish":
        await ask_for_name(update, context)
    elif text == "📤 Jo'natish":
        await send_data(update, context)
    elif text == "📍 Manzil":
        await location_info(update, context)
    elif text == "📞 Bog'lanish":
        await contact_info(update, context)
    elif text == "🔙 Ortga qaytish":
        await start(update, context)
    else:
        await update.message.reply_text("Iltimos, quyidagi tugmalardan birini tanlang.")

# Asosiy bot konfiguratsiyasi
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, receive_contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
