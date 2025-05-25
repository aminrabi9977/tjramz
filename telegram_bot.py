# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     MessageHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     ConversationHandler,
#     filters
# )
# import re
# from datetime import datetime
# import asyncio
# from play import scrape
# from uploader import upload_playwright, convert_crypto_name

# # Define conversation states
# (
#     CHOOSING_AUTH,
#     ENTERING_USERNAME,
#     ENTERING_PASSWORD,
#     CHOOSING_CRYPTO,
#     ENTERING_DATE,
#     ENTERING_TIME,
#     PROCESSING,
#     FINAL_CHOICE
# ) = range(8)

# # Regex patterns for validation
# DATE_PATTERN = r'^\d{4}/\d{2}/\d{2}$'
# TIME_PATTERN = r'^\d{2}:\d{2}:\d{2}$'

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Start the conversation and ask user for input."""
#     await update.message.reply_text(
#         "سلام! به ربات تلگرامی تجارت نیوز خوش امدید."
#     )
#     return await auth_start(update, context)

# async def auth_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Start authentication process."""
#     await update.message.reply_text(
#         "🔑 برای تولید خبر قیمت لحظه ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهی."
#     )
#     await update.message.reply_text("👤 نام کاربری را وارد کنید:")
#     return ENTERING_USERNAME

# async def receive_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Store username and ask for password."""
#     context.user_data['username'] = update.message.text
#     await update.message.reply_text("🔒 رمز عبور را وارد کنید:")
#     return ENTERING_PASSWORD

# async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Process password and attempt login."""
#     context.user_data['password'] = update.message.text
    
#     try:
#         # Simulate authentication check
#         if await check_auth(context.user_data['username'], context.user_data['password']):
#             keyboard = [
#                 [
#                     InlineKeyboardButton("Doge", callback_data="doge"),
#                     InlineKeyboardButton("XRP", callback_data="ripple"),
#                     InlineKeyboardButton("Not", callback_data="not")
#                 ]
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#             await update.message.reply_text(
#                 "نام رمز ارز دیجیتال را انتخاب کنید:",
#                 reply_markup=reply_markup
#             )
#             return CHOOSING_CRYPTO
#         else:
#             await update.message.reply_text("❌ نام کاربری یا رمز عبور نادرست است!")
#             return await auth_start(update, context)
#     except Exception as e:
#         await update.message.reply_text(f"خطا:: {str(e)}")
#         return await auth_start(update, context)

# async def check_auth(username: str, password: str) -> bool:
#     """Verify authentication credentials."""
#     try:
#         # We'll use a simple check here - you might want to enhance this
#         return username and password and len(username) > 2 and len(password) > 2
#     except Exception as e:
#         print(f"خطا: {e}")
#         return False

# async def crypto_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Handle cryptocurrency selection."""
#     query = update.callback_query
#     await query.answer()
    
#     context.user_data['crypto_name'] = query.data
#     await query.message.reply_text(
#         "📅 تاریخ انتشار را وارد کنید( به طور مثال: 1402/02/03):"
#     )
#     return ENTERING_DATE

# async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Process and validate the publication date."""
#     date_text = update.message.text
    
#     if not re.match(DATE_PATTERN, date_text):
#         await update.message.reply_text(
#             "فرمت ورودی نادرست است! مجددا تاریخ انتشار را وارد کنید (فرمت: 1402/02/03):"
#         )
#         return ENTERING_DATE
    
#     context.user_data['publish_date'] = date_text
#     await update.message.reply_text(
#         "⏰ زمان انتشار را وارد کنید (به طور مثال: 10:15:00):"
#     )
#     return ENTERING_TIME

# async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Process and validate the publication time."""
#     time_text = update.message.text
    
#     if not re.match(TIME_PATTERN, time_text):
#         await update.message.reply_text(
#             "فرمت ورودی نادرست است! مجددا زمان انتشار را وارد کنید (فرمت: 10:15:00): "
#         )
#         return ENTERING_TIME
    
#     context.user_data['publish_time'] = time_text
#     await update.message.reply_text("⚙️ در حال پردازش...")
#     return await process_upload(update, context)

# async def process_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Handle the upload process."""
#     try:
#         await update.message.reply_text(f"📊 در حال استخراج قیمت لحظه ای {context.user_data['crypto_name']}")
        
#         crypto_data = await scrape(context.user_data['crypto_name'])
#         if not crypto_data:
#             raise Exception("استخراج اطلاعات با خطا مواجه شد.")
        
#         await update.message.reply_text(
#             "📝 در حال بارگذاری اطلاعات و تولید خبر در تجارت نیوز..."
#         )
        
#         # Combine date and time
#         publish = f"{context.user_data['publish_date']} {context.user_data['publish_time']}"
        
#         # Upload to website
#         await upload_playwright(
#             "https://tejaratnews.com/admin-start-b2dc",
#             context.user_data['username'],
#             context.user_data['password'],
#             context.user_data['crypto_name'],
#             publish
#         )
        
#         await update.message.reply_text("✅ خبر با موفقیت بارگذاری شد.")
        
#         # Show final options
#         keyboard = [
#             [
#                 InlineKeyboardButton(
#                     "انتشار خبر  و استخراج قیمت لحظه ای رمز ارز دیگر",
#                     callback_data="publish_another"
#                 )
#             ],
#             [
#                 InlineKeyboardButton("خروج از حساب", callback_data="exit")
#             ]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await update.message.reply_text(
#             "الان میخواهید چکار کنید:",
#             reply_markup=reply_markup
#         )
#         return FINAL_CHOICE
        
#     except Exception as e:
#         await update.message.reply_text(f"خطا: {str(e)}")
#         return await auth_start(update, context)

# async def handle_final_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Handle user's final choice."""
#     query = update.callback_query
#     await query.answer()
    
#     if query.data == "publish_another":
#         keyboard = [
#             [
#                 InlineKeyboardButton("Doge", callback_data="doge"),
#                 InlineKeyboardButton("XRP", callback_data="ripple"),
#                 InlineKeyboardButton("Not", callback_data="not")
#             ]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await query.message.reply_text(
#             "نام رمز ارز دیجیتال را انتخاب کنید:",
#             reply_markup=reply_markup
#         )
#         return CHOOSING_CRYPTO
#     else:  # exit
#         keyboard = [[InlineKeyboardButton("Login", callback_data="login")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await query.message.reply_text(
#             "تو از صفحه ادمین خارج شده ای.",
#             reply_markup=reply_markup
#         )
#         return CHOOSING_AUTH

# async def handle_login_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Handle login button press after exit."""
#     query = update.callback_query
#     await query.answer()
    
#     await query.message.reply_text(
#         "🔑 برای تولید خبر قیمت لحظه ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهی."
#     )
#     await query.message.reply_text("👤 نام کاربری را وارد کنید:")
#     return ENTERING_USERNAME

# def main() -> None:
#     """Set up and run the bot."""
#     # Replace 'YOUR_BOT_TOKEN' with your actual bot token
#     application = Application.builder().token('7777155817:AAFU51H894E9e-69wWc7GeG-uFMIvt1LuXw').build()

#     conv_handler = ConversationHandler(
#         entry_points=[
#             CommandHandler('start', start),
#             CallbackQueryHandler(handle_login_button, pattern='^login$')
#         ],
#         states={
#             CHOOSING_AUTH: [
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, auth_start),
#                 CallbackQueryHandler(handle_login_button, pattern='^login$')
#             ],
#             ENTERING_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)],
#             ENTERING_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
#             CHOOSING_CRYPTO: [CallbackQueryHandler(crypto_choice)],
#             ENTERING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],
#             ENTERING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_time)],
#             PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_upload)],
#             FINAL_CHOICE: [
#                 CallbackQueryHandler(handle_final_choice, pattern='^(publish_another|exit)$'),
#                 CallbackQueryHandler(handle_login_button, pattern='^login$')
#             ],
#         },
#         fallbacks=[CommandHandler('start', start)]
#     )

#     application.add_handler(conv_handler)
#     application.run_polling()

# if __name__ == '__main__':
#     main()
# -----------------------------------------
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
import re
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright
from play import scrape
from uploader import upload_playwright, convert_crypto_name

# Define conversation states
(
    CHOOSING_AUTH,
    ENTERING_USERNAME,
    ENTERING_PASSWORD,
    CHOOSING_CRYPTO,
    ENTERING_DATE,
    ENTERING_TIME,
    PROCESSING,
    FINAL_CHOICE
) = range(8)

# Regex patterns for validation
DATE_PATTERN = r'^\d{4}/\d{2}/\d{2}$'
TIME_PATTERN = r'^\d{2}:\d{2}:\d{2}$'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "🤖 سلام! به ربات تلگرامی تجارت نیوز خوش امدید."
    )
    return await auth_start(update, context)

async def auth_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start authentication process."""
    await update.message.reply_text(
         "🔑 برای تولید خبر قیمت لحظه ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهی."
    )
    await update.message.reply_text("👤 نام کاربری را وارد کنید:")
    return ENTERING_USERNAME

async def receive_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store username and ask for password."""
    context.user_data['username'] = update.message.text
    await update.message.reply_text("🔒 رمز عبور را وارد کنید:")
    return ENTERING_PASSWORD

async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process password and attempt login."""
    context.user_data['password'] = update.message.text
    
    try:
        await update.message.reply_text("🔄 در حال اعتبارسنجی هویت...")
        
        # Use the same login logic as upload_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            try:
                context_browser = await browser.new_context()
                page = await context_browser.new_page()
                await page.goto("https://tejaratnews.com/admin-start-b2dc")
                
                await page.wait_for_timeout(300)
                await page.fill('input[name="data[name]"]', context.user_data['username'])
                await page.fill('input[name="data[password]"]', context.user_data['password'])
                await page.wait_for_timeout(300)
                await page.click('button[type="submit"]')
                await page.wait_for_timeout(1000)
                
                # Check if login was successful
                if "login" not in page.url:
                    await browser.close()
                    keyboard = [
                        [
                            InlineKeyboardButton("Doge", callback_data="doge"),
                            InlineKeyboardButton("XRP", callback_data="ripple"),
                            InlineKeyboardButton("Not", callback_data="not")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text(
                        "✅ احراز هویت با موفقیت انجام شد.\n💎 نام رمز ارز دیجیتال را انتخاب کنید:",
                        reply_markup=reply_markup
                    )
                    return CHOOSING_CRYPTO
                else:
                    await browser.close()
                    await update.message.reply_text("❌ نام کاربری یا رمز عبور نادرست است!")
                    return await auth_start(update, context)
                
            except Exception as e:
                await browser.close()
                raise e
                
    except Exception as e:
        await update.message.reply_text(f"❌ خطای اعبارسنجی: {str(e)}")
        return await auth_start(update, context)

async def crypto_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle cryptocurrency selection."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['crypto_name'] = query.data
    await query.message.reply_text(
         "📅 تاریخ انتشار را وارد کنید( به طور مثال: 1402/02/03):"
    )
    return ENTERING_DATE

async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process and validate the publication date."""
    date_text = update.message.text
    
    if not re.match(DATE_PATTERN, date_text):
        await update.message.reply_text(
            "⚠️فرمت ورودی نادرست است! مجددا تاریخ انتشار را وارد کنید (فرمت: 1402/02/03):"
        )
        return ENTERING_DATE
    
    context.user_data['publish_date'] = date_text
    await update.message.reply_text(
         "⏰ زمان انتشار را وارد کنید (به طور مثال: 10:15:00):"
    )
    return ENTERING_TIME

async def receive_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process and validate the publication time."""
    time_text = update.message.text
    
    if not re.match(TIME_PATTERN, time_text):
        await update.message.reply_text(
            "⚠️ فرمت ورودی نادرست است! مجددا زمان انتشار را وارد کنید (فرمت: 10:15:00): "
        )
        return ENTERING_TIME
    
    context.user_data['publish_time'] = time_text
    await update.message.reply_text("⚙️ در حال پردازش...")
    return await process_upload(update, context)

async def process_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the upload process."""
    try:
        await update.message.reply_text(f"📊 در حال استخراج قیمت لحظه ای {context.user_data['crypto_name'].upper()}")
        
        crypto_data = await scrape(context.user_data['crypto_name'])
        if not crypto_data:
            raise Exception("استخراج اطلاعات با خطا مواجه شد.")
        
        await update.message.reply_text(
              "📝 در حال بارگذاری اطلاعات و تولید خبر در تجارت نیوز..."
        )
        
        # Combine date and time
        publish = f"{context.user_data['publish_date']} {context.user_data['publish_time']}"
        
        # Call upload_playwright with all the necessary information
        await upload_playwright(
            "https://tejaratnews.com/admin-start-b2dc",
            context.user_data['username'],
            context.user_data['password'],
            context.user_data['crypto_name'],
            publish
        )
        
        await update.message.reply_text("✅ خبر با موفقیت بارگذاری شد.")
        
        # Show final options
        keyboard = [
            [
                InlineKeyboardButton(
                     "انتشار خبر  و استخراج قیمت لحظه ای رمز ارز دیگر",
                    callback_data="publish_another"
                )
            ],
            [
                InlineKeyboardButton("خروج از حساب", callback_data="exit")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
             "الان میخواهید چکار کنید:",
            reply_markup=reply_markup
        )
        return FINAL_CHOICE
        
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")
        return await auth_start(update, context)

async def handle_final_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user's final choice."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "publish_another":
        keyboard = [
            [
                InlineKeyboardButton("Doge", callback_data="doge"),
                InlineKeyboardButton("XRP", callback_data="ripple"),
                InlineKeyboardButton("Not", callback_data="not")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "💎 نام رمز ارز دیجیتال را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return CHOOSING_CRYPTO
    else:  # exit
        keyboard = [[InlineKeyboardButton("Login", callback_data="login")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "👋 تو از صفحه ادمین خارج شده ای.",
            reply_markup=reply_markup
        )
        return CHOOSING_AUTH

async def handle_login_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle login button press after exit."""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
          "🔑 برای تولید خبر قیمت لحظه ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهی."
    )
    await query.message.reply_text("👤 نام کاربری را وارد کنید:")
    return ENTERING_USERNAME

def main() -> None:
    """Set up and run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token('7777155817:AAFU51H894E9e-69wWc7GeG-uFMIvt1LuXw').build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(handle_login_button, pattern='^login$')
        ],
        states={
            CHOOSING_AUTH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, auth_start),
                CallbackQueryHandler(handle_login_button, pattern='^login$')
            ],
            ENTERING_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)],
            ENTERING_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
            CHOOSING_CRYPTO: [CallbackQueryHandler(crypto_choice)],
            ENTERING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],
            ENTERING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_time)],
            PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_upload)],
            FINAL_CHOICE: [
                CallbackQueryHandler(handle_final_choice, pattern='^(publish_another|exit)$'),
                CallbackQueryHandler(handle_login_button, pattern='^login$')
            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()