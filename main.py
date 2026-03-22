import argparse
from modules.identifier import identify
from modules.encodings import decode_hex, decode_base64, decode_base32, decode_binary
from modules.classical import rot13, caesar_bruteforce, xor_bruteforce
from modules.hashes import crack_hash, hash_string

WORDLIST_DEFAULT = (
    "wordlists/rockyou.txt"  # Change it for the direction and the name of your wordlist
)


def cmd_identify(args):
    results = identify(args.text)
    print(f"\nAnalizando: {args.text}\n")
    for r in results:
        confidence_color = {"high": "✅", "medium": "⚠️", "low": "❓"}
        icon = confidence_color.get(r["confidence"], "")
        print(f"  {icon} {r['type']} (confidence: {r['confidence']})")


def cmd_decode(args):
    text = args.text
    dtype = args.type

    decoders = {
        "hex": lambda: decode_hex(text),
        "base64": lambda: decode_base64(text),
        "base32": lambda: decode_base32(text),
        "binary": lambda: decode_binary(text),
        "rot13": lambda: rot13(text),
    }

    if dtype not in decoders:
        print(f" Error: {dtype} not supported")
        return

    result = decoders[dtype]()
    print(f"\n Result: {result}")


def cmd_caesar(args):
    print(f"\n[*] Bruteforce Caesar: {args.text}\n")
    results = caesar_bruteforce(args.text)
    for r in results:
        print(f"  shift {r['shift']:>2}: {r['result']}")


def cmd_xor(args):
    try:
        with open(args.file, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not founded")
        return

    print(f"\nXDR Bruteforce in {args.file}\n")
    results = xor_bruteforce(data)

    if not results:
        print("Not readable results founded")
        return

    for r in results[:10]:
        print(f"  key {r['key']}: {r['result'][:60]}")


def cmd_crack(args):
    wordlist = args.wordlist or WORDLIST_DEFAULT
    print(f"\nCracking: {args.hash}")
    print(f"Wordlist: {wordlist}\n")

    result = crack_hash(args.hash, wordlist)
    if result:
        print(f"Found: {result}")
    else:
        print("Not found in the wordlist")


def cmd_hash(args):
    result = hash_string(args.text, args.algorithm)
    print(f"\n{args.algorithm.upper()}: {result}")
