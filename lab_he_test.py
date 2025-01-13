#####################################################
# COMP0061 Privacy Enhancing Technologies -- Lab on Homomorphic Encryption
#
# Basics of Privacy Friendly Computations through Additive Homomorphic Encryption.
#
# Run the tests through:
# $ pytest -v

#####################################################
# TASK 1 -- Setup, key derivation, log Encryption and Decryption

import pytest
from pytest import raises
from lab_he import *


@pytest.mark.task1
def test_encrypt():
    params = setup()
    priv, pub = key_gen(params)
    assert encrypt(params, pub, 0)
    assert encrypt(params, pub, 99)
    assert encrypt(params, pub, -99)
    with raises(Exception):
        encrypt(params, pub, -100)
    with raises(Exception):
        encrypt(params, pub, 100)


@pytest.mark.task1
def test_decrypt():
    params = setup()
    priv, pub = key_gen(params)
    assert decrypt(params, priv, encrypt(params, pub, 0)) == 0
    assert decrypt(params, priv, encrypt(params, pub, 2)) == 2
    assert decrypt(params, priv, encrypt(params, pub, 99)) == 99


#####################################################
# TASK 2 -- Define homomorphic addition and multiplication with a public value

@pytest.mark.task2
def test_add():
    params = setup()
    priv, pub = key_gen(params)
    one = encrypt(params, pub, 1)
    two = encrypt(params, pub, 2)
    three = add(params, pub, one, two)
    assert decrypt(params, priv, three) == 3

    # Try it for a range of numbers
    for x in range(-10, 10):
        Ex = encrypt(params, pub, x)
        E2x = add(params, pub, Ex, Ex)
        assert decrypt(params, priv, E2x) == 2 * x


@pytest.mark.task2
def test_mul():
    params = setup()
    priv, pub = key_gen(params)
    two = encrypt(params, pub, 2)
    three = mul(params, pub, two, 2)
    assert decrypt(params, priv, three) == 4

    # Try it for a range of numbers
    for x in range(-10, 10):
        enc_x = encrypt(params, pub, x)
        enc_20_x = mul(params, pub, enc_x, 20)
        assert decrypt(params, priv, enc_20_x) == 20 * x


#####################################################
# TASK 3 -- Define Group key derivation & Threshold decryption.
#           Assume an honest but curious set of authorities.

@pytest.mark.task3
def test_group_key():
    params = setup()
    _, _, o = params

    # Generate a group key
    priv1, pub1 = key_gen(params)
    priv2, pub2 = key_gen(params)
    pub = gen_group_key(params, [pub1, pub2])

    # Check it is valid
    priv = (priv1 + priv2) % o
    assert decrypt(params, priv, encrypt(params, pub, 0)) == 0


@pytest.mark.task3
def test_partial():
    params = setup()

    # Generate a group key
    priv1, pub1 = key_gen(params)
    priv2, pub2 = key_gen(params)
    pub = gen_group_key(params, [pub1, pub2])

    # Each authority decrypts in turn
    c = encrypt(params, pub, 0)
    c_prime = partial_decrypt(params, priv1, c)
    m = partial_decrypt(params, priv2, c_prime, True)
    assert m == 0


#####################################################
# TASK 4 -- Actively corrupt final authority, derives a public key with a known private key.

@pytest.mark.task4
def test_bad_pub():
    params = setup()
    g, h, o = params

    # Four authorities generate keys
    priv1, pub1 = key_gen(params)
    priv2, pub2 = key_gen(params)
    priv3, pub3 = key_gen(params)
    priv4, pub4 = key_gen(params)

    # Derive a bad key
    x = Integer.random_range(min_inclusive=1, max_exclusive=o)
    bad_pub = corrupt_pub_key(params, x, [pub1.copy(), pub2.copy(), pub3.copy(), pub4.copy()])

    # Derive the group key including the bad public key
    pub = gen_group_key(params, [pub1, pub2, pub3, pub4, bad_pub])
    assert pub.xy == (g * x).xy

    # Check that the corrupt authority can decrypt a message
    # encrypted under the group key with its secret only.
    assert decrypt(params, x, encrypt(params, pub, 1)) == 1


#####################################################
# TASK 5 -- Implement operations to support a simple private poll.

@pytest.mark.task5
def test_poll():
    votes = [1, 0, 1, 0, 1, 1, 0, 1, 1, 1]
    v0, v1 = simulate_poll(votes)
    assert v0 == 3
    assert v1 == 7
