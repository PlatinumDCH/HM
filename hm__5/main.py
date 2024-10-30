import aiohttp
import asyncio
import platform
from typing import Any

class HttpError(Exception):
    '''custom exception for http errors '''
    pass

class PrivatBankApi:
    base_url ='https://api.privatbank.ua/p24api/exchange_rates?json&date='
    

    async def request(self, date: str)->dict[str, Any]:
        '''get currency exchange rates for a given date'''
        url = f'{self.base_url}{date}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result
                    else:
                        raise HttpError(f"Error status: {resp.status} for {url}")
            except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
                raise HttpError(f'Connection error: {url}', str(err))


async def main():
    try:
        response = await request('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
        return response
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)