import asyncio
from modular_api.api_client import APIClient

async def main():
    api = APIClient("https://jsonplaceholder.typicode.com")
    response = await api.async_request("/posts/1")
    print(response)

asyncio.run(main())
