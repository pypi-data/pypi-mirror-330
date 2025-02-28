from client3x.client3x import InboundPayload

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

print(str_representation)
