from pprint import pprint

from client3x.client3x import CLientPayload


class X3UIPayload(CLientPayload):
    def __init__(self, inbound_id, client_id, email, limitip, expiry_time, subid, custom_field1, custom_field2):
        super().__init__(inbound_id, client_id, email, limitip, expiry_time,subid,
                         additional_fields= {"custom_field1": custom_field1, "custom_field2": custom_field2}  )


def test():
    payload = X3UIPayload(12345, "aaaa-aaaa-aaaa-aaaa", "john.doe@example.com", 3,17000000000, "1234567890", "Custom Field 1", "Custom Field 2")
    pprint(payload.format())


if __name__ == "__main__":
    test()