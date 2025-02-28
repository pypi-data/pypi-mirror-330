import json
import unittest
from client3x.client3x import InboundPayload


class InboundPayloadTest(unittest.TestCase):

    def test_inbound_payload_default_values(self):
        port = 8080
        stream_settings = {"network": "tcp"}

        payload = InboundPayload(port, stream_settings)

        self.assertEqual(payload.data["port"], 8080)
        self.assertEqual(json.loads(payload.data["streamSettings"]), {"network": "tcp"})
        self.assertEqual(payload.data["up"], 0)
        self.assertEqual(payload.data["down"], 0)
        self.assertEqual(payload.data["total"], 0)
        self.assertEqual(payload.data["remark"], "New")
        self.assertTrue(payload.data["enable"])
        self.assertEqual(payload.data["expiryTime"], 0)
        self.assertEqual(payload.data["listen"], "")
        self.assertEqual(payload.data["protocol"], "vless")
        self.assertEqual(json.loads(payload.data["settings"]), {"clients": [], "decryption": "none", "fallbacks": []})
        self.assertEqual(json.loads(payload.data["sniffing"]), {
            "enabled": True,
            "destOverride": ["http", "tls", "quic", "fakedns"],
            "metadataOnly": False,
            "routeOnly": False
        })
        self.assertEqual(json.loads(payload.data["allocate"]), {
            "strategy": "always",
            "refresh": 5,
            "concurrency": 3
        })
    
    def test_inbound_payload_custom_values(self):
        port = 1234
        stream_settings = {"network": "ws", "wsSettings": {"path": "/test"}}
        up = 1000
        down = 2000
        total = 3000
        remark = "Custom Inbound"
        enable = False
        expiry_time = 1234567890
        listen = "127.0.0.1"
        protocol = "vmess"
        settings = {"clients": [{"id": "test-id"}], "disableInsecureEncryption": True}
        sniffing = {"enabled": False, "destOverride": ["http", "tls"]}
        allocate = {"strategy": "random", "refresh": 10, "concurrency": 5}

        payload = InboundPayload(
            port, stream_settings, up, down, total, remark, enable, expiry_time,
            listen, protocol, settings, sniffing, allocate
        )

        self.assertEqual(payload.data["port"], 1234)
        self.assertEqual(json.loads(payload.data["streamSettings"]), {"network": "ws", "wsSettings": {"path": "/test"}})
        self.assertEqual(payload.data["up"], 1000)
        self.assertEqual(payload.data["down"], 2000)
        self.assertEqual(payload.data["total"], 3000)
        self.assertEqual(payload.data["remark"], "Custom Inbound")
        self.assertFalse(payload.data["enable"])
        self.assertEqual(payload.data["expiryTime"], 1234567890)
        self.assertEqual(payload.data["listen"], "127.0.0.1")
        self.assertEqual(payload.data["protocol"], "vmess")
        self.assertEqual(json.loads(payload.data["settings"]), {"clients": [{"id": "test-id"}], "disableInsecureEncryption": True})
        self.assertEqual(json.loads(payload.data["sniffing"]), {"enabled": False, "destOverride": ["http", "tls"]})
        self.assertEqual(json.loads(payload.data["allocate"]), {"strategy": "random", "refresh": 10, "concurrency": 5})

    def test_inbound_payload_str_representation(self):
        port = 8080
        stream_settings = {"network": "tcp"}
        up = 100
        down = 200
        total = 300
        remark = "Test Inbound"
        enable = True
        expiry_time = 1234567890
        listen = "0.0.0.0"
        protocol = "vless"
        settings = {"clients": [{"id": "test-id"}], "decryption": "none"}
        sniffing = {"enabled": True, "destOverride": ["http", "tls"]}
        allocate = {"strategy": "always", "refresh": 5, "concurrency": 3}

        payload = InboundPayload(
            port, stream_settings, up, down, total, remark, enable, expiry_time,
            listen, protocol, settings, sniffing, allocate
        )

        str_representation = str(payload)

        self.assertIn(f"Port: {port}", str_representation)
        self.assertIn(f"Protocol: {protocol}", str_representation)
        self.assertIn(f"Remark: {remark}", str_representation)
        self.assertIn(f"Enabled: {enable}", str_representation)
        self.assertIn(f"Listen: {listen}", str_representation)
        self.assertIn(f"Expiry Time: {expiry_time}", str_representation)
        self.assertIn(f"Up: {up}", str_representation)
        self.assertIn(f"Down: {down}", str_representation)
        self.assertIn(f"Total: {total}", str_representation)
        self.assertIn('"clients": [\n    {\n      "id": "test-id"\n    }\n  ]', str_representation)
        self.assertIn('"decryption": "none"', str_representation)
        self.assertIn('"network": "tcp"', str_representation)
        self.assertIn('"enabled": true', str_representation)
        self.assertIn('"destOverride": [\n    "http",\n    "tls"\n  ]', str_representation)
        self.assertIn('"strategy": "always"', str_representation)
        self.assertIn('"refresh": 5', str_representation)
        self.assertIn('"concurrency": 3', str_representation)


if __name__ == '__main__':
    unittest.main()