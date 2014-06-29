# Birthday Attack: SHA1 Collisions

> This was a team project with two others: Andrew Seitz and Tobias Muller in March 2014 for my cryptography class. Here's the writeup we did.

We implemented the birthday attack by searching across iterations of the uppercase and lowercase ASCII characters, along with numbers.

## Design

The code is written in Python 3.4 and uses the `sha` function from the `hexlib` library to search for collisions. It takes two arguments: the first is the maximum number of random bytes to use as input to the hash function, and the second is the number of bytes needed, starting at the beginning of the hash, for two inputs to be considered a collision.

The way the code works is this: random hashes are generated, and the results of each hash are stored as keys in a dictionary (Python's implementation of the hash table data structure). This allows lookup of collisons for already generated hashes to happen in constant time. When a collision is found, the results are printed to the screen.

## Results

Since the results only took a few seconds to run, we ran the program a few times to generate multiple collisions. We ran more than these, and they generally would have to try about 20 million attempts before a collision was found.

According to Wikipedia^[`https://en.wikipedia.org/wiki/Birthday_attack`] the number of trials required to reach 50% chance of finding a collision can be found by
$$n(0.5,2^{48}) \approx 1.1774 \sqrt{2^{48}} = 19.755 \times 10^6.$$
This is basically in line with the 20 million figure we saw from our test runs.

### Collision #1

``` Bash
$ time python3.4 sha5.py 10 6
Collision found!
b'51c6a3aa723a' hashes to 93c78fb33f70, but b'95a1d9e96e42606284'
also hashes to 93c78fb33f70
Took 19881348 trials
python3.4 sha5.py 10 6  93.49s user 45.17s system 100% cpu 2:18.63 total
```

### Collision #2

Sometimes a collision can be found fairly quickly. This one only took 3.94 seconds, and 1/13 the trials of Collision #1.

``` Bash
$ time python3.4 sha5.py 12 6
Collision found!
b'ce4912bfe6274259' hashes to 82b06260148a, but b'9863780e679e2b2f895a5c'
also hashes to 82b06260148a
Took 1509438 trials
python3.4 sha5.py 12 6  6.86s user 3.94s system 100% cpu 10.799 total
```

### Collision #3

``` Bash
$ time python3.4 sha5.py 8 6
Collision found!
b'957d7a9c41bd85' hashes to e1acf78f4680, but b'f6cccc834bcb5933'
also hashes to e1acf78f4680
Took 15658783 trials
python3.4 sha5.py 8 6  76.45s user 35.57s system 100% cpu 1:52.00 total
```

## Code

``` Python
#!/usr/bin/env python3

from hashlib import sha1
from binascii import hexlify
from itertools import product
from sys import argv
from random import getrandbits, randint
from os import urandom
```

`hashmap` stores our hash dictionary, from SHA1 outputs to SHA1 inputs.

``` Python
hashmap = {}
```

`HASHCHARS` represents the number of characters to consider in the hash function, starting at the beginning. For example, 6 means we use the first 6 bytes of sha1. This is overwritten if a second command-line argument is given; we are asked to look for 6 bytes, so we replace this with 6 when we run it.

``` Python
HASHCHARS = 8
```

`sha1_hash()` returns the shortened SHA1 hash of `s`. If the input is bytes, they will be hashed directly; otherwise they will be encoded to ascii before being hashed.

``` Python
def sha1_hash(s):
    return sha1(s).hexdigest()[:HASHCHARS * 2]

```

`show()` prints the original string and the collision string. It then recompute the hashes of each of them and print those, to prove that we found a collision.

``` Python
def show(right, left):
    # Print stuff.
    print('Collision found!')
    print(str(hexlify(left))
            + ' hashes to ' + str(sha1_hash(left))
            + ', but ' + str(hexlify(right))
            + ' also hashes to ' + str(sha1_hash(right)))
```

`is_collision()` returns true if its input is already in our hashmap. If this succeeds, then we call `show()` on the two collision inputs.

``` Python
def is_collision(bits):
    hash = sha1_hash(bits)
    if hash not in hashmap:
        hashmap[hash] = bits
        return None
    elif not (hashmap[hash] == bits):
        collision = hashmap[hash]
        show(bits, collision)
        return collision
    return None
```

`collide()` runs everything, and calls `show()` if we found a collision. It uses `urandom()` and thus does not get the best possible entropy kernel can offer. This is OK because we are not trying to generate secret keys: we just need numbers that are different to implement the attack. If we generated random numbers from `/dev/random` instead of `/dev/urandom`, we would be limited by the kernel's entropy pool, and the code would take much longer to run.

``` Python
def collide(maxinput=64):
    x = 0
    trial = urandom(randint(1, maxinput))
    while not is_collision(trial):
        # Strip the leading zeros (who cares about zeros!)
        trial = urandom(randint(1, maxinput))
        x += 1
    print('Took ' + str(x) + ' trials')
```

This bit just runs the program. It handles command-line inputs and all that.

``` Python
if __name__ == '__main__':
    if len(argv) > 1:
        n = int(argv[1])
        if len(argv) > 2:
            HASHCHARS=int(argv[2])
        collide(n)
    else:
        collide()
```
