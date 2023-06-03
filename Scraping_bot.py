from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
import asyncio
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import requests
from bs4 import BeautifulSoup

tokenn = '5997435210:AAGv1c7CdZ2rdPwWtOS_rufM6PCQhtHBB2E'

bot = Bot(token=tokenn)
dp = Dispatcher(bot)

url = 'https://funpay.com/chips/99/'  # we take the link of the site we want to parse
take_request = requests.get(url).text  # send a request to the site
soup = BeautifulSoup(take_request, 'lxml')


# The function parses the number of reviews from the seller
def get_count_reviews(count_people):
    reviews = soup.find_all('div', class_="media-user-reviews")
    text_reviews = []
    for review in reviews[:count_people + 1]:
        content = review.get_text().strip()
        if content == 'нет отзывов':
            text_reviews.append('0')
        else:
            text_reviews.append(content)
    return text_reviews


# The function parses the number of available robux from the seller
def get_robux_stoc(count_people):
    values = []
    count_value = soup.find_all('div', class_="tc-amount")
    for value in count_value[:count_people + 1]:
        robux_value = value.get_text().strip()
        if robux_value != 'Наличие':
            values.append(robux_value)
    return values


# The function parses the price for 1 robux from the seller
def get_price_robux(count_people):
    prices = []
    price_rob = soup.find_all('div', class_="tc-price")
    for price in price_rob[:count_people + 1]:
        robux_price = price.get_text().strip()
        if robux_price != 'Цена':
            prices.append(robux_price)
    return prices


# The function parses the link to the seller
def get_user_link(count_people):
    links = []
    links_users = soup.find_all('div', class_="avatar-photo")
    for linki in links_users[:count_people]:
        link_user = linki.get('data-href').strip()
        links.append(link_user)

    return links


# The function parses how much the seller is already trading on the exchange
def get_reg_data(count_people):
    regs_dates = []
    datas = soup.find_all('div', class_="media-user-info")
    for data in datas[:count_people + 1]:
        daty = data.get_text()
        regs_dates.append(daty)

    return regs_dates


@dp.message_handler(Command('start'))
async def first_function(message: types.Message):
    await bot.send_message(message.chat.id, 'Enter how many sellers you want to parse: ')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def parse_command(message: types.Message):
    try:
        count_people = int(message.text)

        reviews = get_count_reviews(count_people)
        robux = get_robux_stoc(count_people)
        robux_price = get_price_robux(count_people)
        user_linkt = get_user_link(count_people)
        data_reg_user = get_reg_data(count_people)

        for review, value, price, user_link, reg_user in zip(reviews, robux, robux_price, user_linkt, data_reg_user):
            output = f'Reviews: {review}\nRobux available: {value}\nPrice for 1 rb: {price}\nLink to profile: {user_link}\nDate of registration: {reg_user}'
            await bot.send_message(message.chat.id, output)

        await bot.send_message(message.chat.id, 'Data successfully parsed')

    except ValueError:
        await bot.send_message(message.chat.id, 'Invalid input!Please enter only integer number')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())
