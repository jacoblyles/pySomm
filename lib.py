import subprocess
from hashlib import sha256
from mnemonic import Mnemonic


def xor_hex_strings(str1, str2):
    """
    Return xor of two hex strings.
    An XOR of two pieces of data will be as random as the input with the most randomness.
    We can thus combine two entropy sources in this way as a safeguard against one source being
    compromised in some way.
    For details, see http://crypto.stackexchange.com/a/17660
    returns => <string> in hex format
    """
    if len(str1) != len(str2):
        print(len(str1), len(str2))
        raise Exception("tried to xor strings of unequal length")
    str1_dec = int(str1, 16)
    str2_dec = int(str2, 16)

    xored = str1_dec ^ str2_dec

    return "{:0{}x}".format(xored, len(str1))


def safety_checklist():

    checks = [
        "Are you running this on a computer WITHOUT a network connection of any kind?",
        "Have the wireless cards in this computer been physically removed?",
        "Are you running on battery power?",
        "Is your screen hidden from view of windows, cameras, and other people?",
        "Are smartphones and all other nearby devices turned off and in a Faraday bag?"]

    for check in checks:
        answer = input(check + " (y/n)?")
        if answer.upper() != "Y":
            print("\n Safety check failed. Exiting.")
            sys.exit()


def get_entropy(length):
    """
    Generate a random string from /dev/random
    """

    print("\n\n")
    print("Retrieving random data....")
    print("If the prompt is stuck, please continually move your mouse cursor.\nThese movements generate entropy which is used to create random data.\n")

    seed = subprocess.check_output(
        "xxd -l {} -p /dev/random".format(length), shell=True)
    seed = seed.decode('ascii').replace('\n', '')
    
    return seed


def validate_dice_seed(dice, min_length):
    """
    Validates dice data (i.e. ensures all digits are between 1 and 6).
    returns => <boolean>
    dice: <string> representing list of dice rolls (e.g. "5261435236...")
    """

    if len(dice) < min_length:
        print("Error: You must provide at least {0} dice rolls".format(min_length))
        return False

    for die in dice:
        try:
            i = int(die)
            if i < 1 or i > 6:
                print("Error: Dice rolls must be between 1 and 6.")
                return False
        except ValueError:
            print("Error: Dice rolls must be numbers between 1 and 6")
            return False

    return True


def read_dice_seed_interactive(min_length=62):
    """
    Reads min_length dice rolls from standard input, as a string of consecutive integers
    Returns a string representing the dice rolls
    returns => <string>
    min_length: <int> number of dice rolls required.  > 0.
    """

    def ask_for_dice_seed(x):
        print("Enter {0} dice rolls (example: 62543 16325 21341...) Spaces are OK, and will be ignored:".format(x))

    ask_for_dice_seed(min_length)
    dice = input()
    dice = unchunk(dice)

    while not validate_dice_seed(dice, min_length):
        ask_for_dice_seed(min_length)
        dice = input()
        dice = unchunk(dice)

    return dice


def validate_mnemonic(mnemonic):
    """
    Validates a BIP39 mnemonic
    Ensures it is a valid length, contains only valid words, and is properly constructed
    returns => <boolean>
    """

    m = Mnemonic("english")

    if not m.check(mnemonic):
        print("Error: Invalid BIP39 mnemonic")
        return False

    return True


def read_mnemonic_interactive():
    """
    Reads a BIP39 mnemonic from standard input, as a string of consecutive words
    Returns a string representing the mnemonic
    """
    
    m = Mnemonic("english")

    def ask_for_mnemonic():
        print("Enter your BIP39 mnemonic")

    ask_for_mnemonic()
    mnemonic = input()


    while not validate_mnemonic(mnemonic):
        ask_for_mnemonic()
        mnemonic = input()

    print("Valid mnemonic. Continuing...")
    return mnemonic


def unchunk(string):
    """
    Remove spaces in string
    """
    return string.replace(" ", "")


def hash_sha256(s):
    """A thin wrapper around the hashlib SHA256 library to provide a more functional interface"""
    m = sha256()
    m.update(s.encode('ascii'))
    return m.hexdigest()

