import base64


class BytesConverter:
    @staticmethod
    def to_base64(data : bytes) -> str:
        return base64.b64encode(data).decode(encoding='utf-8')

    @staticmethod
    def from_base64(data : str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def from_hex(data : str) -> bytes:
        return bytes.fromhex(data)

    @staticmethod
    def to_hex(data : bytes) -> str:
        return data.hex()

    @staticmethod
    def decode(data : bytes) -> str:
        return data.decode()

    @staticmethod
    def encode(data : str) -> bytes:
        return data.encode()