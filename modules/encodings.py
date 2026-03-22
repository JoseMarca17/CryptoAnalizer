import base64


def decode_hex(text: str) -> str:
    clean = text.strip().replace(" ", "").replace("0x", "")
    try:
        return bytes.fromhex(clean).decode("utf-8")
    except UnicodeDecodeError:
        # If it's not readable text, it returns an hex representation of the bytes
        return bytes.fromhex(clean).hex(" ")
    except ValueError as e:
        return f"Error: {e}"


def decode_base64(text: str) -> str:
    try:
        decoded = base64.b64decode(text.strip())
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return decoded.hex(" ")
    except Exception as e:
        return f"Error: {e}"


def decode_base32(text: str) -> str:
    try:
        decoded = base64.b32decode(text.strip().upper())
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return decoded.hex(" ")
    except Exception as e:
        return f"Error: {e}"


def decode_binary(text: str) -> str:
    try:
        clean = text.strip().replace(" ", "")
        # Split into 8-bit chucks and convert each one to a character
        chars = [chr(int(clean[i : i + 8], 2)) for i in range(0, len(clean), 8)]
        return "".join(chars)
    except Exception as e:
        return f"Error: {e}"
