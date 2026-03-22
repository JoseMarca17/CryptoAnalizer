import hashlib


def identify_hash(text: str) -> str:
    hash_lenghts = {
        32: "md5",
        40: "sha1",
        56: "sha224",
        64: "sha256",
        96: "sha384",
        120: "sha512",
    }
    clean = text.strip()
    return hash_lenghts.get(len(clean), "unknown")


def crack_hash(target_hash: str, wordlist_path: str) -> str | None:
    algorithm = identify_hash(target_hash)

    if algorithm == "unknown":
        return None

    hash_func = getattr(hashlib, algorithm)

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip()
                candidate = hash_func(word.encode()).hexdigest()

                if candidate == target_hash.lower():
                    return word
    except FileNotFoundError:
        return f"Eroor: Not founded wordlist in {wordlist_path}"

    return None


def hash_string(text: str, algorithm: str = "md5") -> str:
    try:
        h = hashlib.new(algorithm)
        h.update(text.encode())
        return h.hexdigest()
    except ValueError:
        return f"Error: unsoported '{algorithm}' algorithm"
