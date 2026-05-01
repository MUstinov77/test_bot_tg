import logging
from logging.handlers import RotatingFileHandler

from bot.bot_factory import bot_factory
from bot.core.datastore.session import init_db
from bot.core.config import settings


async def main():

    await init_db()
    
    await bot_factory(settings)



if __name__ == '__main__':
    import asyncio

    logging.basicConfig(
        level=settings.log_level, 
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=(
            RotatingFileHandler(
                filename=settings.log_file_name,
                mode="w", 
                maxBytes=50000000, 
                backupCount=5
            ),
        )
    )
    asyncio.run(main())
    