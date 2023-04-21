import unittest
import json
import main

with open('test/vectors.json') as f:
   vectors = json.load(f)

bech32_pub = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
bech32_address = "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"

class TestStringMethods(unittest.TestCase):

    def test_besch32(self):
        address = main.bech32_for_pubkey(bech32_pub, "bc")
        self.assertEqual(bech32_address, address)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()