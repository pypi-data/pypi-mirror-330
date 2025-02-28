import logging
import uuid



from example_config import *
from client3x import InboundPayload
from client3x.client3x import Client3XUI, CLientPayload, ClientPayload
from client3x.client3x.PanelResponse import PanelResponse




def get_inbounds_example(client: Client3XUI):
    inbounds_resp : PanelResponse = client.get_inbounds()
    print(inbounds_resp)

def get_online_clients(client: Client3XUI):
    online_clients_resp: PanelResponse = client.online_clients()
    print(online_clients_resp)

def reset_traffics_example(client: Client3XUI):
    client.reset_all_traffics()
    print("All clients traffic data reset")


def create_backup_example(client: Client3XUI):
    client.create_backup()
    print("Backup created")

def add_inbound_example(client: Client3XUI):
    inbound_payload = InboundPayload(port = 443,stream_settings={})
    resp: PanelResponse = client.add_inbound(inbound_payload)
    print(resp)

def get_inbound_example(client: Client3XUI):
    resp: PanelResponse = client.get_inbound()
    print(resp)

def update_inbound_example(client: Client3XUI):
    inbound_payload = InboundPayload(port=443, stream_settings={})
    resp: PanelResponse = client.update_inbound(inbound_payload)
    print(resp)

def delete_inbound_example(client: Client3XUI):
    client.delete_inbound()

def reset_all_clients_in_inbound_example(client: Client3XUI):
    client.reset_all_clients_in_inbound()
    print("All clients in inbound reset")

def delete_depleted_example(client: Client3XUI):
    client.delete_depleted_clients()
    print("Depleted clients deleted")

def get_client_traffic(client: Client3XUI, email:str):
    resr: PanelResponse = client.get_client_traffic(email)
    print(f"Client traffic for {email}: {resr}")


def get_client_traffic_by_id_example(client: Client3XUI, client_id:str):
    resr: PanelResponse = client.get_client_traffic_by_id(client_id)
    print(f"Client traffic for {client_id}: {resr}")


def add_client_example(client: Client3XUI, client_payload: ClientPayload):
    link: str = client.add_client(client_payload)
    print(f"Client added: this is his sub link:  {link}")

def update_client_example(client: Client3XUI, client_id, client_payload: ClientPayload):
    link: str = client.update_client(client_id, client_payload)
    print(f"Client updated: this is his sub link:  {link}")

def delete_client_example(client: Client3XUI, client_id):
    client.delete_client(client_id)
    print(f"Client deleted: {client_id}")

def client_ipaddress_example(client: Client3XUI, email: str):
    ip_resp: PanelResponse = client.client_ipaddress(email)
    print(f"Client IP address for {email}: {ip_resp}")

def clear_client_ipaddress_example(client: Client3XUI, email: str):
    client.clear_client_ipadresses(email)
    print(f"Client IP address cleared for {email}")

def reset_client_traffic_example(client: Client3XUI, email: str):
    client.reset_client_traffic(email)
    print(f"Client traffic reset for {email}")

def main():
    client = Client3XUI(
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
    client_id = str(uuid.uuid4())
    email = "new_client@example.com"

    new_client_payload = CLientPayload(
        inbound_id=INBOUND_ID,
        client_id=client_id,
        email=email,
        limitip=5,
        expiry_time=1800000000,
        subid="new_sub_id",
        total_gb=100
    )

    update_payload = CLientPayload(
        inbound_id=INBOUND_ID,
        client_id=client_id,
        email="updated_email@example.com",
        limitip=10,
        expiry_time=1804067200,
        subid="existing_sub_id",
        total_gb=200
    )

    # Retrieve and display a list of all inbounds from the client
    get_inbounds_example(client)

    # Retrieve and display information about a specific inbound from the client
    get_inbound_example(client)

    # Add a new client to the panel using the provided client payload
    add_client_example(client, new_client_payload)

    # Retrieve and display updated information about the inbound (to see the newly added client)
    get_inbound_example(client)

    # Update an existing client's information using the provided client ID and update payload
    update_client_example(client, client_id, update_payload)

    # Retrieve and display traffic information for a specific client using their ID
    get_client_traffic_by_id_example(client, client_id)

    # Retrieve and display the IP address associated with a specific client's email
    client_ipaddress_example(client, email)

    # Clear the IP address information for a specific client using their email
    clear_client_ipaddress_example(client, email)

    # Reset the traffic data for a specific client using their email
    reset_client_traffic_example(client, email)

    # Retrieve and display updated traffic information for the client (after resetting)
    get_client_traffic_by_id_example(client, client_id)

    # Delete a specific client from the panel using their client ID
    delete_client_example(client, client_id)








if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Run the main function
    main()