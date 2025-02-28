from pprint import pprint
from typing import Optional

from client3x.client3x import CLientPayload


def get_payload(inbound_id:int, client_id, email, limitip, expirytime, subid,
             flow="xtls-rprx-vision", total_gb=0, enable=True, reset=0, additional_fields: Optional[dict] = {}):
    """
      Generate a payload dictionary for client configuration.

      This function creates a structured payload containing client information
      for use in API requests or configuration settings.

      Requaried Parameters:
      inbound_id (str): The ID of the inbound connection.
      client_id (str): The unique identifier for the client.
      email (str): The email address associated with the client.
      limitip (int): The maximum number of IP addresses allowed for this client.
      expiryTime (int): The expiration time for the client's access.

      subid (str): The subscription ID for the client.

      Default Parameters:
      flow (str): The TLS/SSL protocol to use for the client's connection.
      totalGB (int): The total storage capacity for the client (in GB).
      enable (bool): Whether the client should be enabled or disabled.
      reset (int): The number of days before the client's access expires.

      Additional Parameters:
      additional_fields (dict): Additional fields to be included in the payload.

      Returns:
      dict: A dictionary containing the structured payload with client information.
            The 'settings' key contains a JSON string with detailed client configuration.
    """

    payload = CLientPayload(inbound_id=inbound_id, client_id=client_id, email=email, limitip=limitip, expiry_time=expirytime, subid=subid,
                            flow = flow, total_gb= total_gb, enable=enable, reset=reset, additional_fields=additional_fields)
    return payload.format()


if __name__ == "__main__":

    # Example usage without custom fields
    payload1 = get_payload(12345, 'aaaa-aaaa-aaaa-aaaa', 'aaaaaaa', 3, 1700000000, 'dbakdahadjwhwadba')
    print('Payload 1 (without custom fields)')
    pprint(payload1)
    print()

    # Example usage with custom fields
    payload2 = get_payload(12345, 'aaaa-aaaa-aaaa-aaaa', 'aaaaaaa', 3, 1700000000, 'dbakdahadjwhwadba', additional_fields={'tgId': 1234567890})
    print('Payload 2 (with custom fields)')
    pprint(payload2)


