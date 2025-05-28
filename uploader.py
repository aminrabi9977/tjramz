
from play import scrape
from playwright.async_api import async_playwright
import asyncio
import time
import jdatetime  
from datetime import datetime  
import pytz  


async def debug_element_visibility(page, selector, description):
    """Debug helper to check element visibility and state"""
    try:
        element = page.locator(selector)
        count = await element.count()
        print(f"Debug {description}: Found {count} elements with selector '{selector}'")
        
        if count > 0:
            is_visible = await element.first.is_visible()
            print(f"Debug {description}: First element visible: {is_visible}")
            
            if selector.startswith('#') and 'input' not in selector:
                # Check if it's a checkbox or radio button
                input_inside = element.locator('input')
                input_count = await input_inside.count()
                if input_count > 0:
                    print(f"Debug {description}: Found {input_count} input elements inside")
        
        return count > 0
    except Exception as e:
        print(f"Debug {description} error: {e}")
        return False

async def set_realTime():
    tehran_tz = pytz.timezone('Asia/Tehran')  
    tehran_time = datetime.now(tehran_tz)

    shamsi_date = jdatetime.date.fromgregorian(date=tehran_time.date()) 

    days_of_week = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]  
    day_of_week = days_of_week[shamsi_date.weekday()]  

    months_names = [  
    "فروردین", "اردیبهشت", "خرداد", "تیر",  
    "مرداد", "شهریور", "مهر", "آبان",  
    "آذر", "دی", "بهمن", "اسفند"    
    ]     
    formatted_date = f"{shamsi_date.day} {months_names[shamsi_date.month - 1]} {shamsi_date.year}"  
    return formatted_date , day_of_week

async def convert_crypto_name(crypto_name):  
    crypto_dict = {  
        'btc': 'بیت کوین',  
        'eth': 'اتریوم',  
        'ripple': 'ریپل',  
        'doge': 'دوج کوین',
        'not' : 'نات کوین',
        'ada': 'کاردانو',
        '1000shib': 'شیبا',
        'trx': 'ترون'
    }  
    return crypto_dict.get(crypto_name.lower())

async def create_news_content(crypto_name, crypto_persian, day_of_week, formatted_date, data):
    """Create news content based on cryptocurrency type"""
    link_url = "https://tejaratnews.com/category/%d8%a7%d8%b1%d8%b2-%d8%af%db%8c%d8%ac%db%8c%d8%aa%d8%a7%d9%84"
    if crypto_name == 'doge':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} ({crypto_name.upper()}) که از لایت کوین فورک شده است؛ اولین میم کوین دنیای کریپتوکارنسی است، و در ابتدا با هدف سرگرمی ساخته شد، اما پس از افزایش محبوبیت توانست با جلب توجه معامله‌گران بازار به یکی از 10 ارز دیجیتال برتر جهان تبدیل شود.

اطلاعات قیمت ارزهای دیجیتال مذکور به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.

            """

    elif crypto_name == 'not':
        content = f"""قیمت {crypto_persian} ({crypto_name.upper()}) یک ارز دیجیتال مبتنی بر فناوری بلاک‌چین است که به عنوان یک پروژه جامعه‌محور و با هدف ایجاد یک اکوسیستم مالی غیرمتمرکز توسعه یافته است. این ارز دیجیتال معمولاً در میان ارزهای دیجیتال با حجم بازار کمتر قرار دارد و به عنوان یک ابزار پرداخت و سرمایه‌گذاری در پلتفرم‌های مختلف استفاده می‌شود.

قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید."""

    elif crypto_name == 'ripple':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} (XRP) یک سیستم تبادل و پرداخت پول است که با هدف بهبود خدمات بانک‌ها ایجاد شده است. و مانند بسیاری از ارزهای دیجیتال دیگر مبتنی بر فناوری بلاک‌چین عمل می‌کند. ریپل یکی از ارزان‌ترین ارزهای دیجیتال موجود در بازارهای جهانی محسوب می‌شود.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود. 

"""

    elif crypto_name == 'btc':
        content = f""" قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} ({crypto_name.upper()}) اولین و یکی از مهم‌ترین رمزارزهای دیجیتال است، که به صورت غیرمتمرکز و مبتنی بر فناوری بلاک‌چین فعالیت می‌کند، و می‌توان از آن برای انتقال ارزش به صورت همتا‌به‌همتا و بدون واسطه استفاده کرد.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.

"""

    elif crypto_name == 'eth':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} (ETH) ارز دیجیتال مبتنی بر فناوری بلاک‌چین است، که با هدف ایجاد امنیت دیجیتال و حذف واسطه‌ها در قراردادها به وجود آمد. استفاده از این ارز پیچیدگی خاصی ندارد و معامله‌گران می‌توانند با افتتاح حساب در یک صرافی شروع به فعالیت کنند.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.
"""

    elif crypto_name == 'ada':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} (ADA) کاردانو(ADA) شبکه‌ای مبتنی بر بلاک‌چین است، که برای انتقال پول دیجیتال و اجرای قراردادهای هوشمند استفاده می‌شود. و به سبب رشد، محبوبیت بسیاری برای سرمایه‌گذاری به دست آورده است.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.
"""

    elif crypto_name == '1000shib':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} (SHIB) شیبا(SHIB) یک رمزارز غیرمتمرکز است، که با الهام گرفتن از دوج کوین ایجاد شده و آن را قاتل دوج کوین معرفی می‌کنند، در واقع شیبا رقیب دوج کوین محسوب می‌شود.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.
"""

    elif crypto_name == 'trx':
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است؛ {crypto_persian} (TRX) یک پلتفرم غیرمتمرکز و مبتنی بر فناوری بلاک‌چین است، که معمولا در میان 10 ارز دیجیتال برتر جهان قرار دارد، و زمینه فعالیت آن غالباً حوزه سرگرمی است.
اطلاعات قیمت ارزهای دیجیتال به صورت لحظه‌ای از صرافی نوبیتکس استخراج شده‌اند.

اخبار حوزه رمزارزها را در صفحه <a href="{link_url}" target="_blank"> ارز دیجیتال </a> تجارت‌نیوز بخوانید.

سلب مسئولیت: همان‌طور که بر همگان روشن است، ورود به معاملات در هر نوع بازاری نیازمند دانش و تجربه‌ کافی است. این گزارش تجارت‌نیوز تنها در راستای تحلیل داده‌ها و اخبار مربوطه است و این مجموعه هیچ‌گونه پیشنهادی برای هر نوع معامله‌ای به خوانندگان محترم ارائه نمی‌دهد؛ همچنین با توجه به نوسانات بالای قیمتی در این بازار لازم است قیمت‌ها در لحظه بررسی شود.
"""

    else:
        # Default content for any new cryptocurrencies
        content = f"""قیمت {crypto_persian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است.

اخبار حوزه رمزارزها را در صفحه ارز دیجیتال تجارت‌نیوز بخوانید."""

    return content
async def upload_playwright_debug(username: str, password: str, crypto_name: str) -> str:
    """Debug version with enhanced error handling and logging"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            context = await browser.new_context(
                viewport={'width': 1366, 'height': 768},
                accept_downloads=True
            )
            context.set_default_timeout(60000)
            page = await context.new_page()

            print("=== Starting WordPress Upload Process ===")

            # Step 1: Login to WordPress
            print("Step 1: Logging in to WordPress...")
            await page.goto("https://tejaratnews.com/wp-login.php", wait_until="networkidle")
            await asyncio.sleep(2)
            
            await page.fill('#user_login', username)
            await asyncio.sleep(1)
            await page.fill('#user_pass', password)
            await asyncio.sleep(1)
            await page.click('#wp-submit')
            
            # Wait for login to complete
            await page.wait_for_url("**/wp-admin/**", timeout=30000)
            print("✅ Login successful")
            await asyncio.sleep(3)
            
            # Step 2: Navigate to new post page
            print("Step 2: Navigating to new post page...")
            await page.goto('https://tejaratnews.com/wp-admin/post-new.php', wait_until="domcontentloaded")
            await asyncio.sleep(5)
            
            # Step 3: Prepare content
            print("Step 3: Preparing content...")
            crypto_persian = await convert_crypto_name(crypto_name)
            formatted_date, day_of_week = await set_realTime()
            
            # Get cryptocurrency data
            data = await scrape(crypto_name)
            print(f"Crypto data: {data}")
            
            # Step 4: Fill in the post details
            print("Step 4: Filling post details...")
            title = f"قیمت {crypto_persian} امروز {day_of_week} {formatted_date}"
            await page.fill('#title', title)
            print(f"✅ Title set: {title}")
            await asyncio.sleep(2)
            
            # Pre-title (روتیتر)
            await page.fill('#rotitr_ak', '«تجارت‌نیوز» گزارش می‌دهد:')
            print("✅ Pre-title set")
            await asyncio.sleep(2)
            
            # Content
            content = await create_news_content(crypto_name, crypto_persian, day_of_week, formatted_date, data)
            print("✅ Content generated")
            
            # Fill content in editor (simplified version for debugging)
            print("Step 5: Adding content to editor...")
            try:
                # Try HTML editor approach first (more reliable)
                html_tab = page.locator('#content-html')
                if await html_tab.is_visible():
                    await html_tab.click()
                    await asyncio.sleep(2)
                    
                    html_textarea = page.locator('#content')
                    await html_textarea.fill(content)
                    await asyncio.sleep(2)
                    print("✅ Content added via HTML editor")
                    
                    # Switch back to visual
                    await page.locator('#content-tmce').click()
                    await asyncio.sleep(3)
                else:
                    print("❌ HTML editor tab not found")
                    
            except Exception as e:
                print(f"❌ Error adding content: {e}")
            
            # Step 6: Set excerpt/summary
            print("Step 6: Setting excerpt...")
            summary = f"قیمت {crypto_persian} {day_of_week} {formatted_date}، در بازار اعلام شد."
            await page.fill('#excerpt', summary)
            print("✅ Excerpt set")
            await asyncio.sleep(2)

            # Step X: Add SEO Focus Keyword (کلمه کلیدی اصلی)
            print("Step X: Setting SEO focus keyword...")
            try:
                # Make sure the Rank Math SEO metabox is visible and expanded
                seo_metabox = page.locator('#rank_math_metabox')
                if await seo_metabox.is_visible():
                    print("Rank Math SEO metabox is visible")
                    
                    # Check if we need to expand the metabox
                    focus_keyword_input = page.locator('.tagify__input')
                    if not await focus_keyword_input.is_visible():
                        print("Need to expand SEO metabox...")
                        toggle = page.locator('#rank_math_metabox .handlediv')
                        await toggle.click()
                        await asyncio.sleep(2)
                    
                    # Find the focus keyword input field (tagify input)
                    focus_keyword_input = page.locator('.tagify__input')
                    if await focus_keyword_input.is_visible():
                        # Click on the input to focus it
                        await focus_keyword_input.click()
                        await asyncio.sleep(1)
                        
                        # Type the Persian cryptocurrency name
                        await focus_keyword_input.type(crypto_persian)
                        await asyncio.sleep(1)
                        
                        # Press Enter to add the keyword
                        await page.keyboard.press('Enter')
                        await asyncio.sleep(2)
                        
                        print(f"✅ Added SEO focus keyword: {crypto_persian}")
                    else:
                        print("❌ Focus keyword input not visible, trying alternative approach...")
            except Exception as e:
                print(f"❌ Error setting content type: {e}")            
            # Step 7: Set content type to "تولیدی"
            print("Step 7: Setting content type...")
            await debug_element_visibility(page, '#metabox_article_type', 'Content Type Metabox')
            await debug_element_visibility(page, '#tolidi_ak', 'Tolidi Radio Button')
            
            try:
                metabox = page.locator('#metabox_article_type')
                if await metabox.is_visible():
                    print("Content type metabox is visible")
                    
                    # Check if we need to expand the metabox
                    tolidi_button = page.locator('#tolidi_ak')
                    if not await tolidi_button.is_visible():
                        print("Need to expand metabox...")
                        toggle = page.locator('#metabox_article_type .handlediv')
                        await toggle.click()
                        await asyncio.sleep(2)
                    
                    # Now try to select تولیدی
                    tolidi_button = page.locator('#tolidi_ak')
                    if await tolidi_button.is_visible():
                        await tolidi_button.check()
                        print("✅ تولیدی selected")
                        await asyncio.sleep(2)
                    else:
                        print("❌ تولیدی button still not visible after expanding")
                        
                        # Try alternative approach
                        await page.evaluate("""
                            const tolidiRadio = document.getElementById('tolidi_ak');
                            if (tolidiRadio) {
                                tolidiRadio.checked = true;
                                console.log('تولیدی selected via JavaScript');
                            }
                        """)
                        await asyncio.sleep(1)
                else:
                    print("❌ Content type metabox not visible")
                    
            except Exception as e:
                print(f"❌ Error setting content type: {e}")
            
            # Step 8: Set categories
            print("Step 8: Setting categories...")
            await debug_element_visibility(page, '#categorydiv', 'Categories Metabox')
            
            try:
                categories_box = page.locator('#categorydiv')
                if not await categories_box.is_visible():
                    toggle_button = page.locator('#categorydiv .handlediv')
                    if await toggle_button.is_visible():
                        await toggle_button.click()
                        await asyncio.sleep(2)
                
                await page.click('a[href="#category-all"]')
                await asyncio.sleep(2)
                print("✅ Switched to 'All Categories' tab")
                
                # Select cryptocurrency-related categories
                crypto_categories = [
                    ('54338', 'ارز دیجیتال'),
                    ('54341', 'اخبار ارز دیجیتال'),
                    ('54745', 'قیمت ارز دیجیتال')
                ]
                
                for cat_id, cat_name in crypto_categories:
                    print(f"Trying to select category: {cat_name} (ID: {cat_id})")
                    
                    # Debug the category checkbox
                    await debug_element_visibility(page, f'#in-category-{cat_id}-2', f'Category {cat_name}')
                    
                    try:
                        selectors = [
                            f'#in-category-{cat_id}-2',
                            f'input[value="{cat_id}"][name="post_category[]"]',
                            f'#in-category-{cat_id}',
                            f'input[type="checkbox"][value="{cat_id}"]'
                        ]
                        
                        found = False
                        for selector in selectors:
                            checkbox = page.locator(selector)
                            if await checkbox.count() > 0:
                                is_checked = await checkbox.is_checked()
                                if not is_checked:
                                    await checkbox.check()
                                    print(f"✅ Successfully checked category {cat_name}")
                                    await asyncio.sleep(1)
                                else:
                                    print(f"✅ Category {cat_name} was already checked")
                                found = True
                                break
                        
                        if not found:
                            print(f"❌ Could not find checkbox for category {cat_name}")
                            
                    except Exception as e:
                        print(f"❌ Error checking category {cat_name}: {e}")
                        
            except Exception as e:
                print(f"❌ Error setting categories: {e}")
            
            # Step 9: Set news sorting
            print("Step 9: Setting news sorting...")
            await debug_element_visibility(page, '#titr_naab_meta', 'News Sorting Metabox')
            
            try:
                news_sorting_box = page.locator('#titr_naab_meta')
                if await news_sorting_box.is_visible():
                    # Check if we need to expand
                    main_checkbox = page.locator('#titr_yek_main')
                    if not await main_checkbox.is_visible():
                        print("Need to expand news sorting metabox...")
                        news_sorting_toggle = page.locator('#titr_naab_meta .handlediv')
                        await news_sorting_toggle.click()
                        await asyncio.sleep(2)
                    
                    # Check main boxes
                    await page.locator('#titr_yek_main').check()
                    print("✅ Checked تیتر یک main")
                    await asyncio.sleep(1)
                    
                    await page.locator('#naab_main').check()
                    print("✅ Checked بخش ناب main")
                    await asyncio.sleep(1)
                    
                    # Check category-specific boxes
                    category_ids_for_sorting = ['54338', '54341', '54745']
                    
                    for category_id in category_ids_for_sorting:
                        try:
                            # Make category fields visible
                            await page.evaluate(f"""
                                var metaFields = document.querySelector("#meta_fields_{category_id}");
                                if (metaFields) {{
                                    metaFields.style.display = "block";
                                }}
                            """)
                            await asyncio.sleep(1)
                            
                            # Check the boxes for this category
                            titr_yek = page.locator(f'#titr_yek_{category_id}')
                            if await titr_yek.count() > 0:
                                await titr_yek.check()
                                print(f"✅ Checked titr_yek for category {category_id}")
                                await asyncio.sleep(0.5)
                            
                            naab = page.locator(f'#naab_{category_id}')
                            if await naab.count() > 0:
                                await naab.check()
                                print(f"✅ Checked naab for category {category_id}")
                                await asyncio.sleep(0.5)
                                
                        except Exception as e:
                            print(f"❌ Error with category-specific news sorting for {category_id}: {e}")
                            
            except Exception as e:
                print(f"❌ Error handling News Sorting section: {e}")
            
            # Step 10: Add tags
            print("Step 10: Adding tags...")
            try:
                tags_box = page.locator('#tagsdiv-post_tag')
                if not await tags_box.is_visible():
                    toggle_button = page.locator('#tagsdiv-post_tag .handlediv')
                    if await toggle_button.is_visible():
                        await toggle_button.click()
                        await asyncio.sleep(2)
                
                # Add cryptocurrency-related tags
                tags = [f'قیمت {crypto_persian}']
                
                for tag in tags:
                    await page.fill('input[name="newtag[post_tag]"]', tag)
                    await asyncio.sleep(1)
                    await page.keyboard.press('Enter')
                    await asyncio.sleep(2)
                    print(f"✅ Added tag: {tag}")
                    
            except Exception as e:
                print(f"❌ Error adding tags: {e}")
            
            # Step 11: Save as draft
            print("Step 11: Saving as draft...")
            await debug_element_visibility(page, '#submitdiv', 'Submit/Publish Box')
            await debug_element_visibility(page, '#save-post', 'Save Draft Button')
            
            try:
                await page.evaluate("window.scrollTo(0, 0);")
                await asyncio.sleep(2)
                
                publish_box = page.locator('#submitdiv')
                
                if not await publish_box.is_visible():
                    print("Submit box not visible, scrolling to it...")
                    await page.evaluate("""
                        const publishBox = document.getElementById('submitdiv');
                        if (publishBox) {
                            publishBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    """)
                    await asyncio.sleep(2)
                
                # Check if the publish box needs to be expanded
                save_button = page.locator('#save-post')
                if not await save_button.is_visible():
                    print("Save button not visible, trying to expand submit box...")
                    toggle_indicator = publish_box.locator('.handlediv')
                    if await toggle_indicator.is_visible():
                        await toggle_indicator.click()
                        await asyncio.sleep(2)
                        print("✅ Expanded submit box")
                
                # Try to click save draft button
                save_button = page.locator('#save-post')
                if await save_button.is_visible():
                    print("✅ Found save draft button, clicking...")
                    await save_button.click()
                    await asyncio.sleep(5)
                    
                    # Wait for save confirmation
                    try:
                        await page.wait_for_selector('#message.updated', timeout=10000)
                        print("✅ Save confirmation message found!")
                    except Exception as e:
                        print(f"No confirmation message found: {e}")
                        # Check if URL changed
                        if 'post.php?post=' in page.url and 'action=edit' in page.url:
                            print("✅ URL changed to edit mode, save likely successful")
                        else:
                            print("⚠️ Could not confirm if save was successful")
                    
                    print("\n🎉 News uploaded successfully as draft!")
                    
                else:
                    print("❌ Save button still not visible, trying JavaScript approach...")
                    result = await page.evaluate("""
                        const saveButton = document.getElementById('save-post');
                        if (saveButton) {
                            saveButton.click();
                            return 'clicked via JS';
                        }
                        
                        const saveByValue = document.querySelector('input[value*="ذخیره"]');
                        if (saveByValue) {
                            saveByValue.click();
                            return 'clicked by value';
                        }
                        
                        return 'no button found';
                    """)
                    print(f"JavaScript result: {result}")
                    await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Error in save draft process: {e}")
                raise
            
            await asyncio.sleep(3)
            return True
                
        except Exception as e:
            print(f"\n❌ Error in upload process: {e}")
            raise e
        finally:
            await browser.close()

# if __name__ == "__main__":
#     # Test the debug uploader
#     import sys
#     if len(sys.argv) > 3:
#         username = sys.argv[1]
#         password = sys.argv[2]
#         crypto = sys.argv[3]
#         asyncio.run(upload_playwright_debug(username, password, crypto))
#     else:
#         print("Usage: python debug_uploader.py <username> <password> <crypto_name>")
#         print("Example: python debug_uploader.py myuser mypass btc")