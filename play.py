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

            # Get page content for BS4
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Extract usdt price
            usdt_container = soup.find(
                'div', class_='text-body-bold-large text-txt-neutral-default dark:text-txt-neutral-default')
            usdt_price = usdt_container.text

            # Extract irt
            irt_container = soup.find(
                'div', class_='text-headline-medium text-txt-neutral-default dark:text-txt-neutral-default desktop:text-headline-large')
            irt_price = irt_container.text

            # Extract 24h change
            change = ''
            change_container = soup.find_all(
                'div', class_='flex flex-wrap items-center gap-8')
            change_value = change_container[0].find(
                'div', class_='rounded-medium')
            if float(change_value.text[:-1]) > 0:
                change = 'افزایش'
            elif float(change_value.text[:-1]) < 0:
                change = 'کاهش'

            data = {
                'usdt_price': usdt_price,
                'irt_price': irt_price,
                'change_24h': float(change_value.text[1:-1]),
                'change_symb': change
            }

            await page.wait_for_timeout(1000)

            return data
        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            await browser.close()


async def main():
    crypto_name = input("Enter cryptocurrency name (e.g., btc, doge): ")

    result = await scrape(crypto_name)
    if result:
        print(f"Cryptocurrency data: {result}")


if __name__ == "__main__":
    asyncio.run(main())
