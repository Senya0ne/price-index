import asyncio
import httpx
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

API_URL = os.getenv("API_URL", "http://price_api:8000")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "👋 Привет!\n\n"
        "Команды:\n"
        "/price <товар> - показать цены\n"
        "/follow <товар> - подписаться на уведомления\n"
        "/unfollow <товар> - отписаться\n\n"
        "Пример:\n"
        "/price xiaomi redmi a27q"
    )

@dp.message(Command("price"))
async def price_command(msg: Message):
    query = msg.text.replace("/price", "").strip()

    if not query:
        await msg.answer("❗ Напиши товар после команды /price")
        return

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            # Получаем результаты поиска
            search_r = await client.get(f"{API_URL}/search/v2", params={"q": query})
            search_r.raise_for_status()
            search_data = search_r.json()
            
            if not search_data.get("results"):
                await msg.answer("😕 Ничего не нашёл")
                return
            
            item = search_data["results"][0]
            canonical = item["product"]
            
            # Получаем лучшую цену
            best_r = await client.get(f"{API_URL}/best-price/", params={"canonical": canonical})
            best_data = best_r.json() if best_r.status_code == 200 else {}
            
            # Получаем статистику
            stats_r = await client.get(f"{API_URL}/price-stats/", params={"canonical": canonical, "days": 30})
            stats_data = stats_r.json() if stats_r.status_code == 200 else {}
            
            # Формируем ответ
            lines = [
                f"📦 *{canonical}*\n",
            ]
            
            if best_data.get("price"):
                lines.append(f"💰 *Лучшая цена:* {int(best_data['price'])} ₽ ({best_data.get('source', 'N/A').capitalize()})")
            
            if stats_data.get("min") is not None:
                lines.append(
                    f"\n📉 *Мин / Сред / Макс (30 дн):*\n"
                    f"{int(stats_data['min'])} / {int(stats_data['avg'])} / {int(stats_data['max'])} ₽"
                )
            
            await msg.answer(
                "\n".join(lines),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(Command("follow"))
async def follow_command(msg: Message):
    query = msg.text.replace("/follow", "").strip()

    if not query:
        await msg.answer("❗ Напиши товар после команды /follow")
        return

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            # Ищем canonical_name
            search_r = await client.get(f"{API_URL}/search/v2", params={"q": query})
            search_r.raise_for_status()
            search_data = search_r.json()
            
            if not search_data.get("results"):
                await msg.answer("😕 Товар не найден")
                return
            
            canonical = search_data["results"][0]["product"]
            
            # Создаём подписку
            sub_r = await client.post(
                f"{API_URL}/subscriptions/",
                params={
                    "user_id": msg.from_user.id,
                    "canonical": canonical,
                    "threshold": 10.0
                }
            )
            
            if sub_r.status_code == 200:
                await msg.answer(f"✅ Подписка создана на *{canonical}*\nУведомлю, когда цена упадёт на 10% или больше", parse_mode="Markdown")
            else:
                await msg.answer("❌ Ошибка при создании подписки")
                
        except Exception as e:
            await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(Command("unfollow"))
async def unfollow_command(msg: Message):
    query = msg.text.replace("/unfollow", "").strip()

    if not query:
        await msg.answer("❗ Напиши товар после команды /unfollow")
        return

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            # Ищем canonical_name
            search_r = await client.get(f"{API_URL}/search/v2", params={"q": query})
            search_r.raise_for_status()
            search_data = search_r.json()
            
            if not search_data.get("results"):
                await msg.answer("😕 Товар не найден")
                return
            
            canonical = search_data["results"][0]["product"]
            
            # Удаляем подписку
            sub_r = await client.delete(
                f"{API_URL}/subscriptions/{msg.from_user.id}",
                params={"canonical": canonical}
            )
            
            if sub_r.status_code == 200:
                await msg.answer(f"✅ Подписка на *{canonical}* удалена", parse_mode="Markdown")
            else:
                await msg.answer("❌ Подписка не найдена")
                
        except Exception as e:
            await msg.answer(f"❌ Ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
