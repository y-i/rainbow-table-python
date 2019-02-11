import hashlib
import pickle
import random

def hex_to_dec(c):
    if 'a' <= c <= 'f':
        return ord(c) - ord('a') + 10
    else:
        return ord(c) - ord('0')

def dec_to_char(i):
    if i < 10:
        return chr(i + ord('0'))
    elif i < 10 + 26:
        return chr(i - 10 + ord('a'))
    elif i < 10 + 26 + 26:
        return chr(i - 10 - 26 + ord('A'))

def reduce_sha256_4(hash, stage):
    num_array = list(map(hex_to_dec, hash))
    for i in range(64):
        if (stage & (1 << i)) == 0:
            continue
        num_array[i] ^= 1
    rolling_hash = [0] * 4
    for i in range(4):
        for j in range(16):
            rolling_hash[i] += num_array[(i*16+j+stage)%64] * 16 ** (16 - 1 - j)
            rolling_hash[i] %= 62
    return "".join(map(dec_to_char, rolling_hash))

def hash_sha256(str):
    return hashlib.sha256(str.encode()).hexdigest()

def create_rainbow_table(l):
    s = l[0]
    for i in range(1500):
        s = reduce_sha256_4(hash_sha256(s), i)
    l.append(s)
    return l

def create_table():
    table = [["".join([dec_to_char(random.randrange(62)) for j in range(4)])] for i in range(10000)]
    table = list(map(create_rainbow_table, table))
    with open('table.pickle', 'wb') as f:
        pickle.dump(table, f)
    return table

def search(table, target):
    for i in reversed(range(1500)):
        if i % 100 == 0:
            print(i)
        hash = target
        for j in range(i, 1500-1):
            hash = hash_sha256(reduce_sha256_4(hash, j))
        reduction = reduce_sha256_4(hash, 1500-1)
        for j in range(10000):
            if (reduction == table[j][1]):
                answer = table[j][0]
                for k in range(1500):
                    if hash_sha256(answer) == target:
                        return answer
                    answer = reduce_sha256_4(hash_sha256(answer), k)
    raise Exception('Not found')

if __name__ == '__main__':
    try:
        with open('table.pickle', 'rb') as f:
            table = pickle.load(f)
    except FileNotFoundError:
        print('Create table -- starts')
        table = create_table()
        print('Create table -- finished')

    print('Answer is ' + search(table, hash_sha256('YAML')))
    print('Answer is ' + search(table, hash_sha256('9JAE')))
    print('Answer is ' + search(table, hash_sha256('hoge')))
