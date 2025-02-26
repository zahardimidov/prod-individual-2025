from os import getenv

from httpx import AsyncClient

YANDEX_CLOUD_API_TOKEN = getenv('YANDEX_CLOUD_API_TOKEN')
YANDEX_CLOUD_ID = getenv('YANDEX_CLOUD_ID')

CLASSIFICATION_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/fewShotTextClassification'
COMPLETION_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


class YandexCloudService:
    def __init__(self):
        self.headers = {
            'Authorization': f'Api-Key {YANDEX_CLOUD_API_TOKEN}'
        }

    async def generate_text(self, advertiser_name, ad_name, min_length=200, max_length=500):
        prompt = f'''
Сгенерируй текст для рекламного объявления исходя из названия рекламодателя и названия самого объявление.
Текст должен содержать от {min_length} до {max_length} символов и завлекать пользователей нажать на рекламу, чтобы воспользоваться предлагаемой услугой
'''
        json = {
            "modelUri": f"gpt://{YANDEX_CLOUD_ID}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "200",
                "reasoningOptions": {
                    "mode": "DISABLED"
                }
            },
            "messages": [
                {
                    "role": "system",
                    "text": prompt
                },
                {
                    "role": "user",
                    "text": f"Рекламодатель: '{advertiser_name}'. Объявление: '{ad_name}'"
                }
            ]
        }

        try:
            async with AsyncClient() as client:
                response = await client.post(COMPLETION_URL, headers=self.headers, json=json)
                print(response.json())
                return response.json()['result']['alternatives'][0]['message']['text']
        except Exception as e:
            print(e)