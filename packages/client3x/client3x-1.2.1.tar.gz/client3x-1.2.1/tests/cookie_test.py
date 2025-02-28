import asyncio
import logging

from client3x import AsyncClient3XUI
from client3x.tests.test_config import *





async def main():
    client = AsyncClient3XUI(
        login=PANEL_LOGIN,
        password=PANEL_PASSWORD,
        login_key=PANEL_SECRET_KEY,
        panel_host=PANEL_HOST,
        root_url=PANEL_ROOT_URL,
        sub_host=SUB_HOST,
        sub_path=SUB_PATH,
        inbound_id=INBOUND_ID,
        panel_port=PANEL_PORT,
        sub_port=SUB_PORT,
        logging_enabled=CLIENT_LOGGING_ENABLED,
        timeout=30
    )

    await client.start()
    print(await client.get_inbounds())
    await asyncio.sleep(60)
    print(await client.get_inbounds())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    asyncio.run(main())
