import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import python_weather

# ВСТАВЬТЕ СЮДА ВАШ ТОКЕН ОТ BOTFATHER
BOT_TOKEN = "123"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обновленная функция получения погоды с красивым оформлением
async def get_weather(city: str) -> str:
    async with python_weather.Client(unit=python_weather.METRIC, locale=python_weather.Locale.RUSSIAN) as client:
        try:
            weather = await client.get(city)

            # Выбираем эмодзи в зависимости от температуры
            if weather.temperature > 25:
                temp_emoji = "🔥"
            elif weather.temperature > 15:
                temp_emoji = "☀️"
            elif weather.temperature > 0:
                temp_emoji = "🌥️"
            else:
                temp_emoji = "❄️"

            # Формируем красивый текст с HTML-тегами
            result_text = (
                f"🌍 <b>Погода в городе {city.capitalize()}</b>\n\n"
                f"{temp_emoji} Температура: <b>{weather.temperature}°C</b>\n"
                f"🤔 Ощущается как: <i>{weather.feels_like}°C</i>\n"
            )
            return result_text

        except Exception as e:
            return "❌ Не удалось найти такой город. Проверьте название."


# Обработчик команды /start (с картинкой и красивым текстом)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Отправляем приветственное сообщение с HTML-разметкой
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! 👋\n\n"
        "Я умею узнавать погоду в любом городе мира. 🌎\n"
        "Просто напиши мне название города (например, <i>Москва</i> или <i>Лондон</i>), и я все расскажу!",
        parse_mode="HTML"  # Включаем режим HTML для этого сообщения
    )


# Обработчик городов
@dp.message()
async def handle_city(message: types.Message):
    city = message.text

    # Отправляем сообщение "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    weather_result = await get_weather(city)

    # Отправляем результат с HTML-разметкой
    await message.answer(weather_result, parse_mode="HTML")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())