import logging
from bot_module import BotFileManager


class AIPhotoManager:
    def __init__(self, client):
        self.__client = client
        logging.basicConfig(level=logging.INFO)

    async def get_mood_by_photo(self, photo_file_name: str):
        image_base64 = await BotFileManager.encode_image(photo_file_name)
        message_payload = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":
                            """Determine the mood in the photo and return the overall
                            mood with a little explanation. The answer must be in Russian"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
        try:
            response = await self.__client.chat.completions.create(
                model="gpt-4o",
                messages=message_payload,
                max_tokens=300,
            )
            content = response.choices[0].message.content
            return str(content)
        except Exception as e:
            logging.error(f'Failed to get mood by photo: {e}')
            return None
