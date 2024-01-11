import asyncio
import logging
import logging.config
from aioconsole import ainput
from telethon.sync import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
import arrow
import re

class TelegramTimeUpdater:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('my_session', api_id, api_hash)
        self.setup_logger()

    @staticmethod
    def setup_logger():
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'level': 'DEBUG',
                },
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console'],
            },
        }
        logging.config.dictConfig(logging_config)

    @staticmethod
    def remove_time_from_string(s):
        return re.sub(r' \d{2}:\d{2}$', '', s)

    async def update_profile(self, client, choice, current_time):
        user_full = await client(GetFullUserRequest(id='me'))
        user = user_full.users[0]
        original_first_name = self.remove_time_from_string(user.first_name)
        original_about = self.remove_time_from_string(user_full.full_user.about)

        if choice == "اسم" or choice == "هردو":
            user.first_name = f"{original_first_name} {current_time}"
        if choice == "بیوگرافی" or choice == "هردو":
            user_full.full_user.about = f"{original_about} {current_time}"
        await client(UpdateProfileRequest(first_name=user.first_name, about=user_full.full_user.about))

    async def update_time(self, choice):
        async with self.client as client:
            current_time = arrow.now().format('HH:mm')
            while True:
                new_time = arrow.now().format('HH:mm')
                if new_time != current_time:
                    current_time = new_time
                    await self.update_profile(client, choice, current_time)

async def main():
    api_id="your api id"
    api_hash="your api hash"
    updater = TelegramTimeUpdater(api_id, api_hash)
    choice = await ainput("میخوای تایم روی اسم باشه یا بیوگرافی یا هردو؟ (اسم/بیوگرافی/هردو): ")
    await updater.update_time(choice)

if __name__ == "__main__":
    asyncio.run(main())
