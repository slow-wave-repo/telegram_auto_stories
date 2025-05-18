#!/usr/bin/env python3

import os
import asyncio

from TelegramAutoStories import TelegramAutoStories, APIInput


if __name__ == '__main__':
    if os.path.isfile('Config.py'):

        from Config import API_ID, API_HASH, CHANNEL_USERNAME

        variables_to_check = ['API_ID', 'API_HASH', 'CHANNEL_USERNAME']

        with open('Config.py', 'r') as c:
            content = c.read()

            if 'API_ID' in content and 'API_HASH' in content and 'CHANNEL_USERNAME' in content:
                tas = TelegramAutoStories(api_id=API_ID,
                                          api_hash=API_HASH,
                                          channel_username=CHANNEL_USERNAME)

                asyncio.run(tas.send())

            else:
                APIInput().write()

                tas = TelegramAutoStories(api_id=API_ID,
                                          api_hash=API_HASH,
                                          channel_username=CHANNEL_USERNAME)
                asyncio.run(tas.send())
    else:

        APIInput().write()

        from Config import API_ID, API_HASH, CHANNEL_USERNAME

        tas = TelegramAutoStories(api_id=API_ID,
                                  api_hash=API_HASH,
                                  channel_username=CHANNEL_USERNAME)
        asyncio.run(tas.send())
