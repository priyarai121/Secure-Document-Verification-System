import base64

def encode_base64(data_bytes):
    """Encodes bytes to a base64 string."""
    return base64.b64encode(data_bytes).decode('utf-8')

def decode_base64(base64_string):
    """Decodes a base64 string back to bytes."""
    return base64.b64decode(base64_string.encode('utf-8'))
