import unittest
import pysomm

bech32_pub = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
bech32_address = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"

class TestStringMethods(unittest.TestCase):

    def test_besch32(self):
        address = pysomm.bech32_for_pubkey(bech32_pub, "bc")
        self.assertEqual(bech32_address, address)

if __name__ == '__main__':
    unittest.main()