from random import randint, seed
from itertools import combinations


SHINGLE_SPACE = 8193
PRIME = 11027
R = 16
B = 64
THR = 0.85


def hashFamily():
    seed(345)

    for _ in range(R * B):
        a = randint(1, PRIME - 1)
        b = randint(0, PRIME - 1)
        yield lambda x: ((a * x + b) % PRIME) % SHINGLE_SPACE

def mapper(key, value):
    # key: None
    # value: one line of input file
    key, values = value.split(' ', 1)

    key = int(key.replace("VIDEO_", ""))
    values = [int(x) for x in values.split(' ')]
    minhash = [min(map(hash, values)) for hash in hashFamily()]

    for index in range(0, R * B, R):
        yield (str(minhash[index: index + R]), (key, values))



def reducer(key, values):

    for a, b in combinations(values, 2):
        key1, shingle1 = a
        key2, shingle2 = b
        shingle1 = set(shingle1)
        shingle2 = set(shingle2)
        sim = float(len(shingle1.intersection(shingle2))) / len(shingle1.union(shingle2))
        if sim >= THR:
            yield (min(key1, key2), max(key1, key2))
