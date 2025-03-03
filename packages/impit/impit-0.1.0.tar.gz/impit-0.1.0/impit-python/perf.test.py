import asyncio
from impit import AsyncClient, Client

async def main():
    impit = AsyncClient(http3=True)

    response = await impit.get(
        "https://curl.se",
        force_http3=True
    );

    print(response.status_code)
    print(response.text)
    print(response.http_version)


asyncio.run(main())
