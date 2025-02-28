import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import mainHandlers, authHandlers, fishHandlers, weatherHandlers

bot = Bot(token=config.TOKEN)

async def main():
    dp = Dispatcher()
    
    dp.include_routers(mainHandlers.mainrt, authHandlers.authrt, fishHandlers.fishrt, weatherHandlers.weatherrt)

    
    print("poling started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())