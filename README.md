[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/H7aqA6IN)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17903139)
[<img alt="points bar" align="right" height="36" src="../../blob/badges/.github/badges/points-bar.svg" /> <img alt="Workflow status" align="right" src="../../workflows/Autograding/badge.svg" />](../../actions/workflows/classroom.yml)

# COMP0061 -- Privacy Enhancing Technologies -- Lab on Homomorphic Encryption

This lab will introduce the basics of Privacy Friendly Computations through Additive Homomorphic Encryption.

### Structure of Labs

The structure of most of the labs will be similar: two Python files will be provided.

- The first is named `lab_X.py` and contains the structure of the code you need to complete.
- The second is named `lab_X_test.py` and contains unit tests (written for the Pytest library) that you may execute to
  partially check your answers.

Note that the tests passing is a necessary but not sufficient condition to fulfill each task. There are programs that
would make the tests pass that would still be invalid (or blatantly insecure) implementations.

The only dependency your Python code should have, besides Pytest and the standard library, is the Pycryptodome library.

The Pycryptodome documentation is [available on-line here](https://www.pycryptodome.org/src/introduction).

### Checking out code

Check out the code by using your preferred git client (e.g., git command line client, GitHub Desktop, Sourcetree).

**_Alternatively_**, you can use the GitHub Codespaces feature to check out and work on the code in the cloud.

### Setup

The intended environment for this lab is the Linux operating system with Python 3 installed.

#### Local virtual environment

To create a local virtual environment, activate the virtual environment, and install the dependencies needed for the
lab, run the following commands in the lab folder:

```shell
python3 -m venv .venv/
source .venv/bin/activate
pip3 install -r requirements.txt
```

On subsequent runs, you will only need to activate the virtualenv.

```shell
source .venv/bin/activate
```

To exit the virtual environment, run:

```shell
deactivate
```

The virtual environment is needed to run the unit tests locally.

#### Development containers

As an alternative to a local virtual environment, we provide the setup files for
[development containers](https://code.visualstudio.com/docs/remote/containers) which use
[Docker](https://docs.docker.com/get-docker/) to create a separate development environment for each repository and
install the required libraries. You don't need to know how to use Docker to use development containers. These are
supported by popular IDEs such as [Visual Studio Code](https://code.visualstudio.com/) and
[PyCharm](https://www.jetbrains.com/pycharm/).

#### GitHub Codespaces

Another alternative for running your code is to use GitHub Codespaces which use cloud-based development containers. On
GitHub, the "<> Code" button at the top right of the repository page will have a Codespaces tab. This allows you to
create a cloud-based environment to work on the assignment. You still need to use `git` to commit and push your work
when working in a codespace.

#### GitHub Classroom tests

The tests are the same as the ones that run as part of the GitHub Classroom automated marking system, so you can also
run the tests by simply committing and pushing your changes to GitHub, without the need for a local setup or even having
Python 3 installed.

### Working with unit tests

Unit tests are run from the command line by executing the command:

```shell
$ pytest -v
```

Note the `-v` flag toggles a more verbose output. If you wish to inspect the output of the full tests run you may pipe
this command to the `less` utility (execute `man less` for a full manual of the less utility):

```shell
$ pytest -v | less
```

You can also run a selection of tests associated with each task by adding the Pytest marker for each task to the Pytest
command:

```shell
$ pytest -v -m task1
```

The markers are defined in the test file and listed in `pytest.ini`.

You may also select tests to run based on their name using the `-k` flag. Have a look at the test file to find out the
function names of each test. For example the following command executes the very first test of Lab 1:

```shell
$ pytest -v -k test_encrypt
```

The full documentation of pytest is [available here](http://pytest.org/latest/).

### What you will have to submit

The deadline for all labs is at the end of term but labs will be progressively released throughout the term, as new
concepts are introduced. We encourage you to attempt labs as soon as they are made available and to use the dedicated
lab time to bring up any queries with the TAs.

Labs will be checked using GitHub Classroom, and the tests will be run each time you push any changes to the `main`
branch of your GitHub repository. The latest score from automarking should be shown in the Readme file. To see the test
runs, look at the Actions tab in your GitHub repository.

Make sure the submitted `lab_he.py` file at least satisfies the tests, without the need for any external dependency
except the Python standard libraries and the Pycryptodome library. Only submissions prior to the GitHub Classroom
deadline will be marked, so make sure you push your code in time.

To re-iterate, the tests passing is a necessary but not sufficient condition to fulfill each task. All submissions will
be checked by TAs for correctness and your final marks are based on their assessment of your work.  
For full marks, make sure you have fully filled in any sections marked with `TODO` comments, including answering any
questions in the comments of the `lab_he.py`.

## TASK 1 -- Additively Homomorphic Encryption \[1 Point\]

> Implement the key generation, encryption and decryption procedures for an additively homomorphic encryption scheme.

## Hints:

- You can run the tests just for this task by executing:

  ```shell
  $ pytest -v -m task1
  ```

- The encryption scheme is the one described in the lectures on private computations.

- Key generation selects a private key between 1 and the order of the group; the public keys is `x * g`, where is a
  generator.

- A ciphertext is composed of two elements: `(k *g, k * pub + m * h)`, where `k` is a random number mod the order of the
  group.

- Do use the table based discrete logarithm function to help implement the decryption operation.

- The `is_ciphertext` function should return True for valid ciphertexts.

## TASK 2 -- Define homomorphic operations on ciphertexts \[1 Point\]

> Implement addition and multiplication by a constant over encrypted data.

## Hints:

- You can run the tests just for this task by executing:

  ```shell
  $ pytest -v -m task2
  ```

- The objective of this task is to perform operations on ciphertext(s) without the knowledge of the secret keys in order
  to generate new ciphertexts that are functions of the original ones.

- The `add` function takes two ciphertexts and should return a ciphertext of the sum of their plaintexts.

- The `mul` function takes a single ciphertext, and returns a fresh ciphertext encrypting a multiple of its plaintext by
  a constant `alpha`.

- Both operations return a ciphertext.

## TASK 3 -- Threshold decryption \[1 Point\]

> Define key derivation and partial decryption to facilitate threshold decryption.

## Hints:

- The `gen_group_key` operation aggregates a list of public keys from a number of authorities, without using any private
  keys, to generate a group public key. Encryption under this group key requires all authorities to help with
  decryption.

- The `partial_decrypt` function takes a ciphertext encrypted under a group public key, and returns a partially
  decrypted ciphertext.

- The `final` flag signifies that an authority is the last in a decryption chain, and should return a plaintext rather
  than a partially decrypted ciphertext.

## TASK 4 -- Corrupt threshold decryption authority \[1 Point\]

> Simulate the operation of a corrupt decryption authority.

## Hints:

- The objective of the function `corrupt_pub_key` is to return a public key that, when combines with other authority
  keys provided, returns a group key that the corrupt authority can decrypt on its own.

- The private key that should decrypt the corrupted group key is provided as an input to the function.

- Have a look at the tests to see an example of the corrupt authority code in action!

## TASK 5 -- A simple polling example \[1 Point\]

> Implement operations to support a simple private poll.

## Hints:

- The `encode_vote` procedure takes a vote (0 or 1) and returns a pair of ciphertexts representing whether it is a vote
  for 0 and whether it is a vote for 1.

- The `process_votes` takes a number of individual pairs of votes and returns a pairs of ciphertexts encrypting the
  total number of votes to 0 and the total number of votes to 1.

- Look at the function `simulate_poll` as a full example of a simulated distributed private poll.

## TASK Qx -- Answer the questions on the basis of your code. \[1 Point\]

> Please include the answers in the comment section provided, and make sure you code file can run correctly.
