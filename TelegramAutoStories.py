#!/usr/bin/env python3

import os
import shutil

from moviepy import VideoFileClip
from telethon import TelegramClient, functions, types, errors
from telethon.tl.types import InputMessagesFilterVideo, InputPeerSelf


class TelegramAutoStories():

    def __init__(self, api_id, api_hash, channel_username):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel_username = channel_username

        self.client = TelegramClient('session', self.api_id, self.api_hash)

        self.download_folder = 'videos'
        os.makedirs(self.download_folder, exist_ok=True)

    async def send(self):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            try:
                phone = input("PHONE NUMBER: ")

                await self.client.send_code_request(phone)

                code = input("CODE: ")

                try:
                    await self.client.sign_in(phone=phone, code=code)

                except errors.SessionPasswordNeededError:
                    password = input("TFA-PASSWORD:")

                    await self.client.sign_in(password=password)

            except Exception as e:
                print(f"ERROR: {e}")

                return

        channel = await self.client.get_entity(self.channel_username)

        messages = self.client.iter_messages(channel,
                                        filter=InputMessagesFilterVideo,
                                        reverse=True)
        counter = 0

        async for message in messages:
            if message.video:
                counter += 1

                print(f'VIDEO: {message.id}')

                file_name = message.file.name if message.file and message.file.name else f"{message.id}.mp4"
                file_path = os.path.join(self.download_folder, file_name)
                path = await message.download_media(file=file_path)
                uploaded = await self.client.upload_file(path)

                clip = VideoFileClip(path)
                duration = int(clip.duration)

                await self.client(functions.stories.SendStoryRequest(
                    peer=InputPeerSelf(),
                    media=types.InputMediaUploadedDocument(
                        file=uploaded,
                        mime_type='video/mp4',
                        attributes=[
                            types.DocumentAttributeVideo(
                                duration=duration,
                                w=720,
                                h=1280,
                                supports_streaming=True
                            )
                        ]
                    ),
                    caption='Sent by TAS-Bot',
                    privacy_rules=[types.InputPrivacyValueAllowAll()]
                ))

                print('DONE!')

                # await client.delete_messages(channel, [message.id])

                print('IN CHANNEL DELETED!')

                break

        if counter == 0:
            print('NO VID')

        if self.download_folder:
            shutil.rmtree(self.download_folder)

        await self.client.disconnect()


class APIInput():

    def write(self):
        if not os.path.isfile('Config.py'):
            with open('Config.py', 'w') as file:
                file.write('')

        a_id = input('API_ID: ')
        b_id = input('API_HASH: ')
        c_id = input('CHANNEL_USERNAME: ')

        lines = ['# Configuration\n',
                 '\n',
                 f'API_ID = {a_id}\n',
                 f'API_HASH = \'{b_id}\'\n',
                 f'CHANNEL_USERNAME = \'{c_id}\'']

        with open('Config.py', 'w') as file:
            file.writelines(lines)

        return

