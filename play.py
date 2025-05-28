
import requests
from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
import json


async def scrape(crypto_name: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            # Navigate to crypto page
            await page.goto(f"https://nobitex.ir/{crypto_name.lower()}/")
            await page.wait_for_timeout(2000)

            # Click on "معامله" button according to code2
            trade_button = page.locator('button[data-value="spot"]')
            await trade_button.click()
            await page.wait_for_timeout(3000)

            # Get page content for BS4 after clicking
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Extract information according to code3 structure
            # Find all trading pairs containers
            trading_containers = soup.find_all('div', class_='flex w-full items-center rounded-large bg-bg-surface-2 px-16 py-20')
            
            usdt_price = None
            irt_price = None
            change_value = None
            change_symb = None
            
            for container in trading_containers:
                # Check if this is USDT pair
                usdt_div = container.find('div', string='USDT')
                if usdt_div:
                    # Get USDT price from the same container
                    price_div = container.find('div', class_='text-body-bold-large')
                    if price_div:
                        usdt_price = price_div.text.strip()
                    
                    # Get change percentage for USDT pair
                    change_div = container.find('div', class_='flex items-center justify-center rounded-medium text-button-medium bg-transparent text-txt-error-default dark:text-txt-error-default')
                    if not change_div:
                        # Try alternative class for positive changes
                        change_div = container.find('div', class_='flex items-center justify-center rounded-medium text-button-medium bg-transparent text-txt-success-default dark:text-txt-success-default')
                    
                    if change_div:
                        change_text = change_div.text.strip()
                        if change_text.startswith('-'):
                            change_symb = 'کاهش'
                            change_value = float(change_text[1:-1])  # Remove - and %
                        elif change_text.startswith('+'):
                            change_symb = 'افزایش'
                            change_value = float(change_text[1:-1])  # Remove + and %
                        else:
                            # If no sign, check if it's in error class (negative) or success class (positive)
                            if 'error' in change_div.get('class', []):
                                change_symb = 'کاهش'
                            else:
                                change_symb = 'افزایش'
                            change_value = float(change_text[:-1])  # Remove %
                
                # Check if this is IRT/Toman pair
                irt_div = container.find('div', string='IRT')
                if irt_div:
                    # Get IRT price from the same container
                    price_div = container.find('div', class_='text-body-bold-large')
                    if price_div:
                        irt_price = price_div.text.strip()

            # If we couldn't find the data with the above method, try alternative approach
            if not usdt_price or not irt_price:
                # Try to find by looking for specific text patterns
                all_price_divs = soup.find_all('div', class_='text-body-bold-large')
                
                for i, div in enumerate(all_price_divs):
                    text = div.text.strip()
                    # Check if this looks like a USDT price (contains comma and is reasonable range)
                    if ',' in text and len(text) < 10:
                        # Look for USDT label nearby
                        parent = div.find_parent()
                        if parent and 'USDT' in parent.get_text():
                            usdt_price = text
                    
                    # Check if this looks like an IRT price (large number)
                    elif ',' in text and len(text) > 10:
                        # Look for IRT label nearby
                        parent = div.find_parent()
                        if parent and 'IRT' in parent.get_text():
                            irt_price = text

            data = {
                'usdt_price': usdt_price or 'N/A',
                'irt_price': irt_price or 'N/A',
                'change_24h': change_value or 0.0,
                'change_symb': change_symb or 'تغییر نامشخص'
            }

            await page.wait_for_timeout(1000)
            return data
            
        except Exception as e:
            print(f"Error in scraping: {e}")
            return {
                'usdt_price': 'N/A',
                'irt_price': 'N/A',
                'change_24h': 0.0,
                'change_symb': 'خطا در دریافت اطلاعات'
            }

        finally:
            await browser.close()


# async def main():
#     crypto_name = input("Enter cryptocurrency name (e.g., btc, eth, doge, ada, 1000shib, not, trx): ")
    
#     result = await scrape(crypto_name)
#     if result:
#         print(f"Cryptocurrency data: {result}")


# if __name__ == "__main__":
#     asyncio.run(main())
