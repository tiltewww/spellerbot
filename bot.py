import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import TOKEN
import requests

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши мне текст, и я проверю его на орфографические ошибки.")

@dp.message()
async def speller(message: types.Message):
    text = message.text.strip()
    
    if not text:
        await message.answer("Пожалуйста, отправьте текст для проверки.")
        return
    
    url = 'https://speller.yandex.net/services/spellservice.json/checkText'
    params = {
        'text': text,
    }
    
    try:
        response = requests.get(url=url, params=params)
        
        if response.status_code != 200:
            await message.answer('Ошибка при обращении к сервису проверки орфографии.')
            return
        
        data = response.json()
        
        if not data:
            await message.answer('Ошибок не найдено.')
            return
        
        errors = []
        for index, error in enumerate(data):
            errors.append(
                'Ошибка №{}. Слово с ошибкой: "{}"; \n Варианты исправления: {}'.format(
                    index + 1,
                    error['word'],
                    ', '.join(error['s'])
                )
            )
        await message.answer("\n\n".join(errors))
    
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())