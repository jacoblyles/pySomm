Welcome to pySomm - a python utility for securely generating new wallets and addresses for the Sommelier blockchain

Warning: this program will generate sensitive data. If an attacker gets ahold of this data, you could lose your keys.

This program should be executed on an **airgapped** computer. To create an airgapped computer:

1. Purchase a new laptop that has not been used for any other purpose
2. Physically remove the wifi card
3. Install Ubuntu Linux on the computer using a USB drive


When you 

* Are you running this on a computer WITHOUT a network connection of any kind?
* Have the wireless cards in this computer been physically removed?
* Are you running on battery power?
* Is your screen hidden from view of windows, cameras, and other people?
* Are smartphones and all other nearby devices turned off and in a Faraday bag?

# Usage

### Generate a seed phrase

```
$ python pysomm.py --genseed [--entropy ENTROPY]
```

The `--entropy` flag is optional. If provided, the entropy must be at least 20 hex digits in length. 

If not provided, pySomm will ask that you use dice rolls to combine with system entropy. Combining outside entropy with system entropy protects against attacks that compromise the system's random number generator. 



### Generate addresses from the seed phrase

