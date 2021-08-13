import aiohttp

MONOBANK_URL: str = "https://api.monobank.ua"
ORIGINAL_HOST: str = "localhost:8000"

def get_header(token: str):
    return { 'X-Token': token }

async def get_user(token: str):
    async with aiohttp.ClientSession() as session:
         async with session.get(f'{MONOBANK_URL}/personal/client-info', headers=get_header(token)) as response:
             return await response.json()

async def set_webhook(token: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{MONOBANK_URL}/personal/webhook', 
            json={'webHookUrl': f'{ORIGINAL_HOST}/api/monobank/recieveTransaction'}, 
            headers=get_header(token)) as response:
                return await response.json()