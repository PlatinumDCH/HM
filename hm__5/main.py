import aiohttp
import asyncio
import platform
from typing import Any
from datetime import datetime, timedelta
import pprint

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
            
    def extract_rates(self, data: dict[str, Any]) -> dict[str, Any]:
        '''Extract EUR and USD rates from API response'''
        rates = {}
        for rate in data.get('exchangeRate', []):
            currency = rate.get('currency')
            if currency in ['EUR', 'USD']:
                rates[currency] = {
                    'sale': rate.get('saleRateNB', None),
                    'purchase': rate.get('purchaseRateNB', None)
                }
        return rates

async def main():
    api_client = PrivatBankApi()
    date = '01.12.2014'
    response = await api_client.request(date)
    rates = api_client.extract_rates(response)
    final_format = [{date: rates}]
    pprint.pprint(final_format)
   
   


if __name__ == '__main__':
    # if platform.system() == 'Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    