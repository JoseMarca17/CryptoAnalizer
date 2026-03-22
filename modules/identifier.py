import re
import base64
import string


def identify(text: str) -> list[dict]:
    """
    It recibes a string and return a list of possible identifications
    Each identidication is a dict with "type" and "confidence" (high/medium/low).
    """

    results = []
    text = text.strip()

    _check_hex(text, results)
    _check_base64(text, results)
    _check_base32(text, results)
    _check_rot13(text, results)
    _check_hash(text, results)
    _check_binary(text, results)

    if not results:
        results.append({"type": "unknow", "confidence": "low"})

    return results


def _check_hex(text: str, results: list):

    # Hex: Characters 0-9 and a-f, even lenght

    clean = text.replace(" ", "").replace("Ox", "")
    if re.fullmatch(r"[0-9a-fA-F]+", clean) and len(clean) % 2 == 0:
        results.append({"type": "hex", "confidence": "high"})


def _check_base64(text: str, results: list):

    # Base64: Alphanumeric characters + +/= and lenght that is a multiple of 4

    if re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", text) and len(text) % 4 == 0:
        try:
            decoded = base64.b64decode(text)
            decoded.decode("utf-8")
            results.append({"type": "base64", "confidence": "high"})
        except Exception:
            results.append({"type": "base64", "confidence": "medium"})


def _check_base32(text: str, results: list):

    # base32: Capital letters only A -Z and 2 - 7, padding with =

    if re.fullmatch(r"[A-Z2-7]+=*", text) and len(text) % 8 == 0:
        results.append({"type": "base32", "confidence": "high"})


def _check_rot13(text: str, results: list):

    # ROT13: Letters and spaces only, heuristic for radability of teh result

    if re.fullmatch(r"[A-Za-z\s\.,!?]+", text):
        decoded = text.translate(
            str.maketrans(
                string.ascii_uppercase + string.ascii_lowercase,
                string.ascii_uppercase[13:]
                + string.ascii_uppercase[:13]
                + string.ascii_lowercase[13:]
                + string.ascii_lowercase[:13],
            )
        )

        if _looks_like_english(decoded):
            results.append({"type": "rot13", "confidence": "high"})
        else:
            results.append({"type": "rot13", "confidence": "low"})


def _check_hash(text: str, results: list):

    # hashes are identified by their lenght and charset hex

    clean = text.strip()
    hash_lengths = {
        32: "md5",
        40: "sha1",
        56: "sha24",
        64: "sha256",
        96: "sha384",
        128: "sha512",
    }

    if re.fullmatch(r"[0-9a-fA-F]+", clean) and len(clean) in hash_lengths:
        results.append(
            {"type": f"hash: {hash_lengths[len(clean)]}", "confidence": "high"}
        )


def _check_binary(text: str, results: list):

    # BInary: 0 and 1 only, lenght that is multiple of 8

    clean = text.replace(" ", "")
    if re.fullmatch(r"[01]+", clean) and len(clean) % 8 == 0:
        results.append({"type": "binary", "confidence": "high"})


def _looks_like_english(text: str) -> bool:

    # Simple heuristic: Common word in English

    common = {"the", "and", "is", "in", "it", "of", "to", "a", "that", "this"}
    words = set(text.lower().split())
    return len(common & words) >= 2
