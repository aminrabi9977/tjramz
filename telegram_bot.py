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
from uploader import upload_playwright_debug, convert_crypto_name

# Define conversation states
(
    CHOOSING_AUTH,
    ENTERING_USERNAME,
    ENTERING_PASSWORD,
    CHOOSING_CRYPTO,
    PROCESSING,
    FINAL_CHOICE
) = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "🤖 سلام! به ربات تلگرامی تجارت‌نیوز خوش آمدید."
    )
    return await auth_start(update, context)

async def auth_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start authentication process."""
    await update.message.reply_text(
         "🔑 برای تولید خبر قیمت لحظه‌ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهید."
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
        
        # Use WordPress login verification
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                context_browser = await browser.new_context()
                page = await context_browser.new_page()
                await page.goto("https://tejaratnews.com/wp-login.php", wait_until="networkidle")
                
                await page.fill('#user_login', context.user_data['username'])
                await asyncio.sleep(1)
                await page.fill('#user_pass', context.user_data['password'])
                await asyncio.sleep(1)
                await page.click('#wp-submit')
                await page.wait_for_timeout(3000)
                
                # Check if login was successful
                if "wp-admin" in page.url:
                    await browser.close()
                    # Create enhanced cryptocurrency keyboard with new currencies
                    keyboard = [
                        [
                            InlineKeyboardButton("Bitcoin (BTC)", callback_data="btc"),
                            InlineKeyboardButton("Ethereum (ETH)", callback_data="eth")
                        ],
                        [
                            InlineKeyboardButton("Ripple (XRP)", callback_data="ripple"),
                            InlineKeyboardButton("Dogecoin (DOGE)", callback_data="doge")
                        ],
                        [
                            InlineKeyboardButton("Cardano (ADA)", callback_data="ada"),
                            InlineKeyboardButton("Shiba Inu (SHIB)", callback_data="shib")
                        ],
                        [
                            InlineKeyboardButton("Tron (TRX)", callback_data="trx"),
                            InlineKeyboardButton("Notcoin (NOT)", callback_data="not")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text(
                        "✅ احراز هویت با موفقیت انجام شد.\n💎 رمز ارز دیجیتال مورد نظر خود را انتخاب کنید:",
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
        await update.message.reply_text(f"❌ خطای اعتبارسنجی: {str(e)}")
        return await auth_start(update, context)

async def crypto_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle cryptocurrency selection."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['crypto_name'] = query.data
    
    # Get crypto name in Persian for display
    crypto_persian = await convert_crypto_name(query.data)
    
    await query.message.reply_text(
         f"📊 {crypto_persian} ({query.data.upper()}) انتخاب شد.\n⚙️ در حال پردازش و تولید خبر..."
    )
    return await process_upload(update, context)

async def process_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the upload process."""
    try:
        crypto_name = context.user_data['crypto_name']
        crypto_persian = await convert_crypto_name(crypto_name)
        
        # Determine if this is from callback query or message
        if update.callback_query:
            message_handler = update.callback_query.message
        else:
            message_handler = update.message
        
        await message_handler.reply_text(f"📊 در حال استخراج قیمت لحظه‌ای {crypto_persian}...")
        
        # Get cryptocurrency data
        crypto_data = await scrape(crypto_name)
        if not crypto_data or crypto_data['usdt_price'] == 'N/A':
            raise Exception("استخراج اطلاعات با خطا مواجه شد.")
        
        # Display extracted data to user
        await message_handler.reply_text(
            f"📈 اطلاعات استخراج شده:\n"
            f"💰 قیمت USDT: {crypto_data['usdt_price']}\n"
            f"💰 قیمت تومان: {crypto_data['irt_price']}\n"
            f"📊 تغییرات 24 ساعته: {crypto_data['change_symb']} {crypto_data['change_24h']}%"
        )
        
        await message_handler.reply_text(
              "📝 در حال بارگذاری اطلاعات و تولید خبر در تجارت‌نیوز..."
        )
        
        # Call upload_playwright without date/time parameters
        await upload_playwright_debug(
            context.user_data['username'],
            context.user_data['password'],
            crypto_name
        )
        
        await message_handler.reply_text("✅ خبر با موفقیت در تجارت‌نیوز بارگذاری شد.")
        
        # Show final options
        keyboard = [
            [
                InlineKeyboardButton(
                     "📊 تولید خبر برای رمز ارز دیگر",
                    callback_data="publish_another"
                )
            ],
            [
                InlineKeyboardButton("🚪 خروج از حساب", callback_data="exit")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message_handler.reply_text(
             "🎯 حالا می‌خواهید چه کاری انجام دهید؟",
            reply_markup=reply_markup
        )
        return FINAL_CHOICE
        
    except Exception as e:
        # Determine message handler for error case
        if update.callback_query:
            message_handler = update.callback_query.message
        elif update.message:
            message_handler = update.message
        else:
            print(f"❌ Error in process_upload: {str(e)}")
            return CHOOSING_CRYPTO
            
        await message_handler.reply_text(f"❌ خطا در پردازش: {str(e)}")
        
        # Return to crypto selection instead of re-authentication
        keyboard = [
            [
                InlineKeyboardButton("Bitcoin (BTC)", callback_data="btc"),
                InlineKeyboardButton("Ethereum (ETH)", callback_data="eth")
            ],
            [
                InlineKeyboardButton("Ripple (XRP)", callback_data="ripple"),
                InlineKeyboardButton("Dogecoin (DOGE)", callback_data="doge")
            ],
            [
                InlineKeyboardButton("Cardano (ADA)", callback_data="ada"),
                InlineKeyboardButton("Shiba Inu (SHIB)", callback_data="1000shib")
            ],
            [
                InlineKeyboardButton("Tron (TRX)", callback_data="trx"),
                InlineKeyboardButton("Notcoin (NOT)", callback_data="not")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message_handler.reply_text(
            "💎 لطفاً رمز ارز دیگری را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return CHOOSING_CRYPTO

async def handle_final_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user's final choice."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "publish_another":
        keyboard = [
            [
                InlineKeyboardButton("Bitcoin (BTC)", callback_data="btc"),
                InlineKeyboardButton("Ethereum (ETH)", callback_data="eth")
            ],
            [
                InlineKeyboardButton("Ripple (XRP)", callback_data="ripple"),
                InlineKeyboardButton("Dogecoin (DOGE)", callback_data="doge")
            ],
            [
                InlineKeyboardButton("Cardano (ADA)", callback_data="ada"),
                InlineKeyboardButton("Shiba Inu (SHIB)", callback_data="1000shib")
            ],
            [
                InlineKeyboardButton("Tron (TRX)", callback_data="trx"),
                InlineKeyboardButton("Notcoin (NOT)", callback_data="not")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "💎 رمز ارز دیجیتال مورد نظر خود را انتخاب کنید:",
            reply_markup=reply_markup
        )
        return CHOOSING_CRYPTO
    else:  # exit
        keyboard = [[InlineKeyboardButton("🔑 ورود مجدد", callback_data="login")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "👋 شما از پنل ادمین خارج شدید.\nبرای استفاده مجدد، دکمه ورود را فشار دهید.",
            reply_markup=reply_markup
        )
        return CHOOSING_AUTH

async def handle_login_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle login button press after exit."""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
          "🔑 برای تولید خبر قیمت لحظه‌ای رمز ارز دیجیتال باید ابتدا عملیات احراز هویت را انجام دهید."
    )
    await query.message.reply_text("👤 نام کاربری را وارد کنید:")
    return ENTERING_USERNAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "🚫 عملیات لغو شد. برای شروع مجدد از دستور /start استفاده کنید."
    )
    return ConversationHandler.END

def main() -> None:
    """Set up and run the bot."""
    # Replace with your actual bot token
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
            PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_upload)],
            FINAL_CHOICE: [
                CallbackQueryHandler(handle_final_choice, pattern='^(publish_another|exit)$'),
                CallbackQueryHandler(handle_login_button, pattern='^login$')
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('cancel', cancel)
        ]
    )

    application.add_handler(conv_handler)
    
    print("🤖 ربات تلگرام تجارت‌نیوز راه‌اندازی شد...")
    application.run_polling()

if __name__ == '__main__':
    main()

# ---------------------------------------------------------------------------
