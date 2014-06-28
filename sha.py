#!/usr/bin/env python3

from hashlib import sha1
from binascii import hexlify
from itertools import product
from sys import argv

POSSIBLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Number of characters to consider in the hash function, starting at the
# beginning. e.g. 6 means we use the first 6 bytes of sha1.
HASHCHARS = 12

def sha1_hash(s):
    ''' Returns the shortened sha1 hash of s. If the input is bytes, they
        will be hashed directly; otherwise they will be encoded to ascii
        before being hashed.
    '''
    if type(s) is bytes:
        # Already encoded, just hash the bytes.
        return sha1(s).hexdigest()[:HASHCHARS]
    else:
        # Convert it to ascii, then hash.
        return sha1(s.encode('ascii')).hexdigest()[:HASHCHARS]

def show(orig_str, collision_str):
    ''' Print the original string, the collision string, and then recompute
        the hashes of each of them and print those, to prove that we found
        a collision.
    '''
    # Do the encoding to ascii for bytes output
    orig_ascii = orig_str.encode('ascii')
    collision_ascii = collision_str.encode('ascii')

    # Print stuff.
    print('Collision found!')
    print(orig_str 
            + ' (bytes: ' + str(hexlify(orig_ascii)) + ')'
            + ' hashes to ' + str(sha1_hash(orig_ascii))
            + ', but ' + collision_str
            + ' (bytes: ' + str(hexlify(collision_ascii)) + ')'
            + ' also hashes to ' + str(sha1_hash(collision_ascii)))

def is_collision(trial, orig_hash):
    ''' Returns true if the hash of trial is the same as orig_hash.
    '''
    h = sha1_hash(trial)
    return h == orig_hash

def collide(startnumber):
    ''' Search for collisions in the hash. Start with the possible match
        at index startnumber and look for collisions by searching upward
        from there.
        Note that this means if you choose a large value (e.g. 400000) this
        will not look for collisions on possibilities 0 <= x <= 400001, so
        choose a low number unless you want this to run for quite a while.
    '''
    # Iterator that yields possible characters.
    possible = product(POSSIBLE, repeat=100)

    # Iterate over the product until we reach the specified startnumber
    for i in range(startnumber):
        possible.__next__()

    # This is our collision target
    orig = ''.join([e for e in possible.__next__()]).lstrip('0')
    orig_hash = sha1_hash(orig)

    # Iterate over the possible options
    for trial in possible:

        # Convert the tuple from itertools.product into a string
        trial = ''.join([e for e in trial])
        # Strip the leading zeros (who cares about zeros!)
        trial = trial.lstrip('0')
        
        # Exit if we found a collision
        if is_collision(trial, orig_hash):
            show(orig, trial)
            break

if __name__ == '__main__':
    if len(argv) > 1:
        n = int(argv[1])
        if len(argv) > 2:
            HASHCHARS=int(argv[2])
        collide(n)
    else:
        print('Please pass an integer as the argument to this program.')
        print()
        print('This number will be used as the starting offset on the string')
        print('search function. It is recommended not to use something like')
        print('"0", since this will end up searching for collisions on the')
        print('empty string ("").')
        print()
        print('e.g.:')
        print('    $ python3 sha.py 300')
        print()
        print('This will search for collisions on the string "4Q", the 301st')
        print('iteration of our cartesian product search algorithm on a')
        print('subset of the ASCII alphabet.')

