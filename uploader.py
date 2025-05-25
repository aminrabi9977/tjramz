# -*- coding: utf-8 -*-
from play import scrape
from playwright.async_api import async_playwright
import asyncio
import time
import jdatetime  
from datetime import datetime  
import pytz  


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
        'bit': 'بیت‌ کوین',  
        'ethereum': 'اتریوم',  
        'ripple': 'ریپل',  
        'doge': 'دوج‌ کوین',
        'not' : 'نات کوین'  
    }  
    return crypto_dict.get(crypto_name.lower())
async def selected_services():
    finall_services = []
    dig_services = ['ارز دیجیتال'  , 'اخبار ارز دیجیتال']
    # select_services = input("which services: ")
    finall_services.append(dig_services)
    return finall_services   

async def upload_playwright(url: str, username: str, password: str, crypto_name: str, publish: str) -> str:
    
      async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            context = await browser.new_context()  
            page = await context.new_page() 
            await page.goto(url)

            # username , passw = await auth()
            await page.wait_for_timeout(300)
            await page.fill('input[name="data[name]"]', username)  # نام کاربری خود را وارد کنید    'a.rabiee'
            await page.fill('input[name="data[password]"]', password)  # رمز عبور خود را وارد کنید   'nMytkC4umX77'
            await page.wait_for_timeout(300)
            await page.click('button[type="submit"]')

           
            if "login" not in page.url:
                cryptoNamePersian = await convert_crypto_name(crypto_name)
                formatted_date, day_of_week = await set_realTime()
                services_list = await selected_services()

                await page.goto('https://tejaratnews.com/fa/admin/newsstudios/add/')
                await page.wait_for_timeout(1000)
                
                data = await scrape(crypto_name)
                
                # Rest of your existing upload logic remains the same
                await page.fill("input[name='data[Newsstudio][newsstudio_data][upTitle]']", "تجارت‌نیوز گزارش می‌دهد:")
                await page.fill('textarea[name="data[Newsstudio][title]"]', f"قیمت {cryptoNamePersian} امروز {day_of_week} {formatted_date}")
                await page.fill('textarea[name="data[Newsstudio][newsstudio_data][lead]"]', f"قیمت {cryptoNamePersian} {day_of_week} {formatted_date}، در بازار اعلام شد.")
                
                # Content logic based on crypto_name
                if (crypto_name == 'doge'):
                    content = f"""قیمت {cryptoNamePersian} {day_of_week} {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است. {cryptoNamePersian} ({crypto_name.upper()})  که از لایت کوین فورک شده است؛ اولین میم کوین دنیای کریپتوکارنسی است و در ابتدا با هدف سرگرمی ساخته شد، اما پس از افزایش محبوبیت توانست با جلب توجه معامله گران بازار به یکی از 10 ارز دیجیتال برتر جهان تبدیل شود.
                    اخبار حوزه رمزارزها را در صفحه ارز دیجیتال تجارت نیوز بخوانید.
                    """
                elif (crypto_name == 'not'):
                    content = f""" قیمت {cryptoNamePersian} {day_of_week}، {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است. {cryptoNamePersian} ({crypto_name.upper()})  یک ارز دیجیتال مبتنی بر فناوری بلاک‌چین است که به عنوان یک پروژه جامعه‌محور و با هدف ایجاد یک اکوسیستم مالی غیرمتمرکز توسعه یافته است. این ارز دیجیتال معمولاً در میان ارزهای دیجیتال با حجم بازار کمتر قرار دارد و به عنوان یک ابزار پرداخت و سرمایه‌گذاری در پلتفرم‌های مختلف استفاده می‌شود. """
                elif (crypto_name == 'ripple'):
                    content = f""" قیمت {cryptoNamePersian} {day_of_week}، {formatted_date}، به سطح {data['usdt_price']} تتر معادل {data['irt_price']} تومان رسیده که با {data['change_symb']} {data['change_24h']} درصدی نسبت به دیروز همراه بوده است. {cryptoNamePersian} (XRP)  یک سیستم تبادل و پرداخت پول است که با هدف بهبود خدمات بانک‌ها ایجاد شده است. و مانند بسیاری از ارزهای دیجیتال دیگر مبتنی بر فناوری بلاک‌چین عمل می‌کند. ریپل یکی از ارزان‌ترین ارزهای دیجیتال موجود در بازارهای جهانی محسوب می‌شود. """

                # Continue with the rest of your existing upload logic
                await page.wait_for_selector("#cke_NewsstudioContentContent iframe")
                editor_frame = page.frame_locator("#cke_NewsstudioContentContent iframe")
                await editor_frame.locator("body").evaluate("element => element.innerHTML = ''")
                await editor_frame.locator("body").type(content)

                for service in services_list[0]:
                    await page.fill("#s2id_autogen13", service)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(100)

                await page.wait_for_timeout(3000)    
                await page.select_option("#NewsstudioPositionFront", "2")  
                await page.select_option("select[name='data[Newsstudio][order][front][position]']", "1")
                
                position_selectors = await page.query_selector_all(".position-category")
                order_selectors = await page.query_selector_all("[data-category-order]")
                
                for pos_selector, ord_selector in zip(position_selectors, order_selectors):
                    await pos_selector.select_option("2")  
                    await ord_selector.select_option("1")  
                    
                await page.wait_for_timeout(1000)    

                await page.fill('#s2id_autogen16', 'رمز ارز')
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

                await page.select_option("#NewsstudioNewsstudioType", "1")  
                await page.select_option("#NewsstudioNewsstudioProductiontype", "1")  
    
                await page.wait_for_timeout(3000)
                await page.fill('#NewsstudioPublishTime', publish)
                await page.wait_for_timeout(1000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.click('button[name = "submit"]')
                await page.wait_for_timeout(3000)
                
                return True
            else:
                raise Exception("Login failed or incorrect page!")
                
        except Exception as e:
            print(f"\nerror: {e}")
            raise e
        finally:
            await browser.close()

if __name__ == "__main__":
    # This section is now mainly for testing
    asyncio.run(upload_playwright("https://tejaratnews.com/admin-start-b2dc"))
