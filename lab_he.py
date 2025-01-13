#####################################################
# COMP0061 Privacy Enhancing Technologies -- Lab on Homomorphic Encryption
#
# Basics of Privacy Friendly Computations through Additive Homomorphic Encryption.
#
# Run the tests with:
# $ pytest -v
from functools import cache

from Cryptodome.Math.Numbers import Integer
from Cryptodome.PublicKey import ECC, _point

curves = _point._curves

Order = Integer
Generator = ECC.EccPoint
Params = tuple[Generator, Generator, Order]
CipherText = tuple[ECC.EccPoint, ECC.EccPoint]

PrivKey = Integer
PubKey = ECC.EccPoint


#####################################################
# TASK 1 -- Setup, key derivation, log Encryption and Decryption

@cache
def setup() -> Params:
    group = curves["secp224r1"]
    o: Order = group.order
    g: Generator = group.G * Integer.random_range(min_inclusive=1, max_exclusive=o)
    h: Generator = group.G * Integer.random_range(min_inclusive=1, max_exclusive=o)
    return g, h, o


def key_gen(params: Params) -> tuple[PrivKey, PubKey]:
    g, h, o = params

    # TODO: ADD CODE HERE
    ...
    priv = ...
    pub = ...
    return priv, pub


def encrypt(params: Params, pub: PubKey, m: int) -> CipherText:
    m = Integer(m)
    if not -100 < m < 100:
        raise Exception("Message value too low or high.")

    g, h, o = params
    # TODO: ADD CODE HERE
    ...
    c = ...
    return c


def _point_to_bytes(p: ECC.EccPoint) -> bytes:
    x, y = p.xy
    return x.to_bytes() + y.to_bytes()


_logh = None


def logh(params: Params, hm: ECC.EccPoint) -> Integer:
    """Compute a discrete log, for small number only"""
    global _logh
    g, h, o = params

    # Initialize the map of logh
    if _logh is None:
        _logh = {}
        for m in range(-1000, 1000):
            m = Integer(m)
            _logh[_point_to_bytes(h * (m % o))] = m
    try:
        return _logh[_point_to_bytes(hm)]
    except KeyError:
        raise Exception("No decryption found.")


def decrypt(params: Params, priv: PrivKey, ciphertext: CipherText) -> Integer:
    # TODO: ADD CODE HERE
    ...
    hm = ...

    return logh(params, hm)


#####################################################
# TASK 2 -- Define homomorphic addition and multiplication with a public value

def add(params: Params, pub: PubKey, c1: CipherText, c2: CipherText) -> CipherText:
    """Given two ciphertexts compute the ciphertext of the sum of their plaintexts."""

    # TODO: ADD CODE HERE
    ...
    c3 = ...
    return c3


def mul(params: Params, pub: PubKey, c1: CipherText, alpha: int) -> CipherText:
    """Given a ciphertext compute the ciphertext of the product of the plaintext times alpha"""

    # TODO: ADD CODE HERE
    ...
    c3 = ...
    return c3


#####################################################
# TASK 3 -- Define Group key derivation & Threshold decryption.
#           Assume an honest but curious set of authorities.

def gen_group_key(params: Params, pub_keys: list[PubKey]):
    """Generate a group public key from a list of public keys"""

    # TODO: ADD CODE HERE
    ...
    pub = ...

    return pub


def partial_decrypt(params: Params, priv: PrivKey, ciphertext: CipherText, final: bool = False) -> Integer | CipherText:
    """Given a ciphertext and a private key, perform partial decryption.
    If final is True, then return the plaintext."""

    # TODO: ADD CODE HERE
    ...
    a1 = ...
    b1 = ...

    if final:
        return logh(params, b1)
    else:
        return a1, b1


#####################################################
# TASK 4 -- Actively corrupt final authority, derives a public key with a known private key.

def corrupt_pub_key(params: Params, priv: Integer, other_pub_keys: list[ECC.EccPoint]) -> PubKey:
    """Simulate the operation of a corrupt decryption authority.
    Given a set of public keys from other authorities return a public key for the corrupt authority that leads to a group
    public key corresponding to a private key known to the corrupt authority."""
    g, h, o = params

    # TODO: ADD CODE HERE
    ...
    pub = ...

    return pub


#####################################################
# TASK 5 -- Implement operations to support a simple private poll.

def encode_vote(params: Params, pub: PubKey, vote: int) -> tuple[CipherText, CipherText]:
    """Given a vote 0 or 1, encode the vote as two ciphertexts representing the count of votes for zero and the votes for one."""
    assert vote in [0, 1]

    # TODO: ADD CODE HERE
    ...
    v0 = ...
    v1 = ...

    return v0, v1


def process_votes(params: Params, pub: PubKey, encrypted_votes: list[tuple[CipherText, CipherText]]) -> tuple[CipherText, CipherText]:
    """Given a list of encrypted votes tally them to sum votes for zeros and votes for ones."""
    assert isinstance(encrypted_votes, list)

    # TODO: ADD CODE HERE
    ...
    tv0 = ...
    tv1 = ...

    return tv0, tv1


def simulate_poll(votes: list[int]) -> tuple[Integer, Integer]:
    """Simulates the full process of encrypting votes, tallying them, and then decrypting the total."""
    # Generate parameters for the crypto-system
    params = setup()

    # Make keys for 3 authorities
    priv1, pub1 = key_gen(params)
    priv2, pub2 = key_gen(params)
    priv3, pub3 = key_gen(params)
    pub = gen_group_key(params, [pub1, pub2, pub3])

    # Simulate encrypting votes
    encrypted_votes = []
    for v in votes:
        encrypted_votes.append(encode_vote(params, pub, v))

    # Tally the votes
    total_v0, total_v1 = process_votes(params, pub, encrypted_votes)

    # Simulate threshold decryption
    privs = [priv1, priv2, priv3]
    for priv in privs[:-1]:
        total_v0 = partial_decrypt(params, priv, total_v0)
        total_v1 = partial_decrypt(params, priv, total_v1)

    total_v0 = partial_decrypt(params, privs[-1], total_v0, True)
    total_v1 = partial_decrypt(params, privs[-1], total_v1, True)

    # Return the plaintext values
    return total_v0, total_v1


###########################################################
# TASK Q1 -- Answer questions regarding your implementation
#
# Consider the following game between an adversary A and honest users H1 and H2:
# 1) H1 picks 3 plaintext integers Pa, Pb, Pc arbitrarily, and encrypts them to the public key of H2 using the scheme
#    you defined in TASK 1.
# 2) H1 provides the ciphertexts Ca, Cb and Cc to H2 who flips a fair coin b.
#    In case b=0 then H2 homomorphically computes C as the encryption of Pa plus Pb.
#    In case b=1 then H2 homomorphically computes C as the encryption of Pb plus Pc.
# 3) H2 provides the adversary A, with Ca, Cb, Cc and C.
#
# What is the advantage of the adversary in guessing b given your implementation of Homomorphic addition?
# What are the security implications of this?

""" TODO: Your Answer here """

###########################################################
# TASK Q2 -- Answer questions regarding your implementation
#
# Given your implementation of the private poll in TASK 5, how would a malicious user implement encode_vote to
# (a) disrupt the poll so that it yields no result, or
# (b) manipulate the poll so that it yields an arbitrary result.
# Can those malicious actions be detected given your implementation?

""" TODO: Your Answer here """
