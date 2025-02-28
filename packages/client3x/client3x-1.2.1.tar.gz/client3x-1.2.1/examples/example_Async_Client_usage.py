import asyncio
import logging
import uuid

from client3x.client3x import AsyncClient3XUI, CLientPayload

from example_config import *

async def main():
    # Initialize the client
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
        logging_enabled=CLIENT_LOGGING_ENABLED
    )

    await client.start()


    client_id = str(uuid.uuid4())
    # Add a new client to the inbound
    new_client_payload = CLientPayload(
        inbound_id=INBOUND_ID,
        client_id = client_id,
        email="client@example.com",
        limitip=5,
        expiry_time=1800000000,  # Example timestamp in milliseconds
        subid="new_sub_id",
        total_gb=100
    )

    new_client_sublink = await client.add_client(new_client_payload)
    print(f"New client added. Subscription link: {new_client_sublink}")

    # Get all clients in the inbound
    clients = await client.get_clients_in_inbound()
    print(f"Total clients in inbound: {len(clients)}")

    # Get info about a specific client
    client_info = await client.get_client_traffic_by_id("existing_client_id")
    if client_info:
        print(f"Client info: {client_info}")

    # Update an existing client
    update_payload = CLientPayload(
        inbound_id=INBOUND_ID,
        client_id=client_id,
        email="client@example.com",
        limitip=10,
        expiry_time=1804067200,  # Example new timestamp
        subid="new_sub_id",
        total_gb=200
    )

    updated_sublink = await client.update_client(client_id, update_payload)
    print(f"Client updated. Subscription link: {updated_sublink}")

    # Delete a client
    await client.delete_client("client_to_delete_id")
    print("Client deleted")

    # Delete depleted clients
    await client.delete_depleted_clients()
    print("Depleted clients deleted")

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Run the async main function
    asyncio.run(main())