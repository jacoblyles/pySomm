import argparse
import sys
from mnemonic import Mnemonic
from bip32 import BIP32
from bech32 import encode as bech32_encode
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from lib import xor_hex_strings, get_entropy, safety_checklist, read_dice_seed_interactive, hash_sha256, \
read_mnemonic_interactive


PRIVATE = None

def generate_mnemonic(entropy):
    if not entropy:
        entropy = read_dice_seed_interactive()
    computer_entropy = get_entropy(20) # 160 bits of entropy
    total_entropy = xor_hex_strings(hash_sha256(entropy), hash_sha256(computer_entropy))
    mnemonic = Mnemonic('english').to_mnemonic(bytes.fromhex(total_entropy))
    return mnemonic


def seed_from_bip39(words):
    seed = Mnemonic('english').to_entropy(words)
    return seed


def address_num(seed, idx):
    """
    Returns the bech32 address for the given index, 
    at the derivation path "m/44'/118'/0'/0/[idx]"
    """
    wallet = BIP32.from_seed(seed)
    pub_key = wallet.get_pubkey_from_path("m/44'/118'/0'/0/{}".format(idx)).hex()
    bech32_address = bech32_for_pubkey(pub_key, "somm")
    return bech32_address


def return_addresses(words, idx=None):
    seed = seed_from_bip39(words)
    if not idx:
        for i in range(5):
            print(address_num(seed, i))
    else:
        print(address_num(seed, idx))


def bech32_for_pubkey(pubkey, hrp="somm"):
    shad = sha256(bytes.fromhex(pubkey)).digest()
    ripe = RIPEMD160.new()
    ripe.update(shad)
    riped = ripe.digest()
    return bech32_encode(hrp, 0, riped)
    

def print_menu():
    print("\nWhat would you like to do?")
    print("1. Generate the next address")
    print("2. Generate an address at a specific index")
    print("3. Exit")


def interactive_loop():
    mnemonic = read_mnemonic_interactive()
    seed = seed_from_bip39(mnemonic)
    address_idx = 0
    seed = seed_from_bip39(mnemonic)
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            print(address_num(seed, address_idx))
            address_idx += 1
        elif choice == "2":
            chosen_idx = int(input("Enter the index: "))
            print(address_num(seed, chosen_idx))
        elif choice == "3":
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    parser = argparse.ArgumentParser(description="BIP39 Mnemonic Tool")
    parser.add_argument("--genseed", action="store_true", help="Output a new BIP39 mnemonic")
    parser.add_argument("--entropy", metavar="ENTROPY", type=str, help="Provide external entropy as a 32-byte hexadecimal string")
    
    parser.add_argument("--addresses", metavar="MNEMONIC", type=str, help="Return first 5 addresses from BIP39 mnemonic")
    parser.add_argument("--idx", metavar="index", type=int, help="Return address at specific index")
    
    parser.add_argument("--login", action="store_true", help="login to your wallet with a mnemonic")
    args = parser.parse_args()

    if args.entropy:
        try:
            if len(args.entropy) < 20:
                raise ValueError("Entropy must be at least 20 hex chars long")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    if args.genseed:
        safety_checklist()
        mnemonic = generate_mnemonic(args.entropy)
        print(f"Generated BIP39 mnemonic: {mnemonic}")

    if args.addresses:
        print("addresses")
        if args.idx:
            return_addresses(args.addresses, args.idx)
        else:
            return_addresses(args.addresses)

    if args.login:
        interactive_loop()

if __name__ == "__main__":
    main()
