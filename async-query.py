import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

AUTH = os.environ.get("HARPER_AUTH_TOKEN")
url = "https://quote-api-vyvyvi.harperdbcloud.com"

payload = """{
    "operation": "sql",
    "sql":"SELECT * FROM dev.quotes where Author = 'eddie_jaoude'"
}"""

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Basic {AUTH}'
}

import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            print(await resp.text().encode('utf8'))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


"""
response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
"""
