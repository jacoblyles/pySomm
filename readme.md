Welcome to pySomm - a python utility for securely generating new wallets and addresses for the Sommelier blockchain

Warning: this program will generate sensitive data. If an attacker gets ahold of this data, you could lose your coins that are stored in these addresses. 

# Hardware Requirements

This program should be executed on an **airgapped** computer that is properly prepared. The airgapped computer will need to have Docker installed. 

1. Purchase a new laptop that has not been used for any other purpose
2. Physically remove the wifi card
3. Install a Linux distribution on the computer using a thumb drive

# Physical Security

When you use pySomm to generate a mnemonic seed, it will prompt you with the following safety checklist:

* Are you running this on a computer WITHOUT a network connection of any kind?
* Have the wireless cards in this computer been physically removed?
* Are you running on battery power?
* Is your screen hidden from view of windows, cameras, and other people?
* Are smartphones and all other nearby devices turned off and in a Faraday bag?
* Are you using casino-grade dice, or some other source of reliable entropy?

These steps are important to eliminate side channels that an attacker can use to steal your coins

## Room Shielding

Any operations involving your seed phrase should be conducted in a room shielded against electromagnetic radiation. If such a room cannot be procured on an immediate basis, a large box covered in aluminum foil should suffice.


# Installation

## For Testing

To install for local testing purposes on a non-airgapped machine, clone this repository and then run
```
$ pip install -r requirements.txt
```
Then you will be able to run commands such as 
```
$ python pysomm.py --help
```
Python 3.8 or higher is required


## Distributing to the airgapped machine

To install on the airgapped machine, you will first clone this repository on a preparation computer with internet access. The preparation machine should be a fresh machine, unused for any other purpose, with a Linux system installed with Docker. We will use this machine to create the **Docker Distribution Image**

To create the Docker Distribution Image, in the project directory run the following commands:

```
$ docker build -t pysomm .
$ docker save -o pysomm.tar pysomm
```
The `.tar` file can be copied to a thumb drive and taken to the airgapped computer. Once loaded onto the airgapped computer, it can be loaded using:

```
$ docker load -i pysomm.tar
```

Once the docker image is loaded onto the airgapped machines, all pySomm commands can be run with a  modification. Instead of running `$ python pysomm.py [command]`, use the following:

```
$ docker run --tty --interactive pysomm pysomm.py [command]
```


# Usage

### Generate a seed phrase

```
$ python pysomm.py --genseed [--entropy ENTROPY]
```

The `--entropy` flag is optional. If provided, the entropy must be at least 20 hex digits in length. You may use whatever high-quality source of entropy that you like, such as a hardware entropy source. 

If not provided, pySomm will ask that you use dice rolls to combine with system entropy. You should use [casino-grade dice](https://www.amazon.com/Trademark-Poker-Grade-Serialized-Casino/dp/B00157YFJE/) to ensure that the dice are unbiased and provide high-quality entropy.

Combining outside entropy with system entropy protects against attacks that compromise the system's random number generator. 


### Generate addresses from the seed phrase

