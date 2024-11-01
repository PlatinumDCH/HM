import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import httpx
from datetime import datetime, timedelta
from app_bank import config
from aiofile import AIOFile
from aiopath import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log_file_path = Path("server.log")


async def request(url: str) -> dict | str:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            return "I couldn't find out the rate. The private mail is not responding :)"


async def log_exchange_command(name: str, days: int, exchange_info: str):
    log_message = f"{datetime.now()} - {name} requested an exchange rate for {days} day(s):\n{exchange_info}\n"
    async with AIOFile(log_file_path, 'a') as afp:
        await afp.write(log_message)


async def get_exchange(days: int = 1) -> str:
    base_url_pb: str = config.APISettings.base_url.value
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(days)]
    results = []

    for date in dates:
        url = f'{base_url_pb}{date}'
        response = await request(url)
        if isinstance(response, dict) and 'exchangeRate' in response:
            rates = response['exchangeRate']
            formatted_rates = {rate['currency']: rate for rate in rates if rate['currency'] in ["USD", "EUR"]}
            results.append(f"{date}\n" + "\n".join(
                [f"     {cur}: Sale - {data['saleRateNB']}, Purchase - {data['purchaseRateNB']}" for cur, data in
                 formatted_rates.items()]))
        else:
            results.append(f"{date} - The course is unavailable")

    return "\n\n".join(results)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                parts = message.split()
                days = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                if days < 1 or days > 10:
                    await self.send_to_clients(f"{ws.name}, the number of days should be between 1 and 10.")
                    continue

                exchange_info = await get_exchange(days)
                await self.send_to_clients(f"{ws.name} requested an exchange rate for {days} day(s):\n{exchange_info}")

                await log_exchange_command(ws.name, days, exchange_info)
            elif message == 'Hello server':
                await self.send_to_clients("Hello There!")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())