import json
from client3x.client3x.payload import Payload

class InboundPayload(Payload):
    def __init__(self,port, stream_settings, up=0, down=0, total=0, remark="New", enable=True, expiry_time=0,
                 listen="",  protocol="vless", settings=None, sniffing=None, allocate=None):
        data = {
            "up": up,
            "down": down,
            "total": total,
            "remark": remark,
            "enable": enable,
            "expiryTime": expiry_time,
            "listen": listen,
            "port": port,
            "protocol": protocol,
            "settings": json.dumps(settings) if settings else json.dumps({
                "clients": [],
                "decryption": "none",
                "fallbacks": []
            }),
            "streamSettings": json.dumps(stream_settings),
            "sniffing": json.dumps(sniffing) if sniffing else json.dumps({
                "enabled": True,
                "destOverride": ["http", "tls", "quic", "fakedns"],
                "metadataOnly": False,
                "routeOnly": False
            }),
            "allocate": json.dumps(allocate) if allocate else json.dumps({
                "strategy": "always",
                "refresh": 5,
                "concurrency": 3
            })
        }
        super().__init__(data)


    def __str__(self):
        def format_json(json_str):
            try:
                return json.dumps(json.loads(json_str), indent=2)
            except json.JSONDecodeError:
                return json_str

        formatted_data = {
            key: format_json(value) if key in ['settings', 'streamSettings', 'sniffing', 'allocate'] else value
            for key, value in self.data.items()
        }

        return (f"InboundPayload:\n"
                f"  Port: {formatted_data['port']}\n"
                f"  Protocol: {formatted_data['protocol']}\n"
                f"  Remark: {formatted_data['remark']}\n"
                f"  Enabled: {formatted_data['enable']}\n"
                f"  Listen: {formatted_data['listen']}\n"
                f"  Expiry Time: {formatted_data['expiryTime']}\n"
                f"  Traffic:\n"
                f"    Up: {formatted_data['up']}\n"
                f"    Down: {formatted_data['down']}\n"
                f"    Total: {formatted_data['total']}\n"
                f"  Settings:\n{formatted_data['settings']}\n"
                f"  Stream Settings:\n{formatted_data['streamSettings']}\n"
                f"  Sniffing:\n{formatted_data['sniffing']}\n"
                f"  Allocate:\n{formatted_data['allocate']}")
