import string


def rot13(text: str) -> str:
    return text.translate(
        str.maketrans(
            string.ascii_uppercase + string.ascii_lowercase,
            string.ascii_uppercase[13:]
            + string.ascii_uppercase[:13]
            + string.ascii_lowercase[13:]
            + string.ascii_lowercase[:13],
        )
    )


def caesar_decrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
        elif char.islower():
            result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
        else:
            result.append(char)

    return "".join(result)


def caesar_bruteforce(text: str) -> list[dict]:
    return [{"shift": i, "result": caesar_decrypt(text, i)} for i in range(1, 26)]


def xor_bruteforce(data: bytes) -> list[dict]:
    results = []

    for key in range(256):
        decrypted = bytes([b ^ key for b in data])
        try:
            text = decrypted.decode("utf-8")
            if _is_printable(text):
                results.append({"key": hex(key), "result": text})
        except UnicodeDecodeError:
            continue

    return results


def _is_printable(text: str) -> bool:
    printable = set(string.printable)
    # At leat 90% of characters should be printable
    ratio = sum(1 for c in text if c in printable) / len(text)
    return ratio > 0.9
