import pprint
from typing import Optional

from client3x.client3x.payload import Payload


class CLientPayload(Payload):

    """
    ClientPayload class for creating or updating inbound clients in a VPN or proxy service.
    """

    def __init__(self, inbound_id: int, client_id: str, email: str, limitip: int,
                 expiry_time: float, subid: str, flow: str = "xtls-rprx-vision",
                 total_gb: int = 0, enable: bool = True, reset: int = 0,
                 additional_fields: Optional[dict] = None):
        """
        Initialize a ClientPayload object with specified client settings.

        This constructor creates a payload with a single client configuration,
        which can be used for creating or updating inbound clients in a VPN or
        proxy service.

        :param inbound_id: int: The ID of the inbound connection.
        :param client_id: str: The unique identifier for the client.
        :param email: str : The email address associated with the client.
        :param limitip: int: The maximum number of simultaneous IP connections allowed.
        :param expiry_time: int|float : The timestamp when the client's access expires.
        :param subid: str: The subscription ID for the client.
        :param flow: Optional[str] : The flow setting for the client. Defaults to "xtls-rprx-vision".
        :param total_gb: Optional[int] :  The total allowed traffic in gigabytes. Defaults to 0 (unlimited).
        :param enable: Optional[bool] :  Whether the client is enabled. Defaults to True.
        :param reset: Optional[int] :  The reset interval for traffic statistics. Defaults to 0.
        :param additional_fields: Optional[dict] :   Additional fields to include in the client settings.

        """

        settings = {"clients" : [
            { "id": client_id,
              "flow": flow,
              "email": email,
              "limitIp": limitip,
              "totalGB": total_gb,
              "expiryTime": expiry_time,
              "enable": enable,
              "subId": subid,
              "reset": reset}
        ]}

        settings["clients"][0].update(additional_fields) if additional_fields else settings["clients"][0]

        data = {"inbound" : inbound_id, "settings": settings}
        super().__init__(data)

    def __str__(self):
        return f'ClientPayload: \nInbound: {self.data['inbound']},\nSettings: {pprint.pformat(self.data['settings'])})'