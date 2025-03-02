import os


def bytes_length(n):
    return (len(bin(n)) - 2 + 7) // 8


def random_int(n):
    ret = n
    while ret >= n:
        l = bytes_length(n)
        bs = os.urandom(l)
        ret = int.from_bytes(bs, byteorder="big")
    return ret


def choice(candidate):
    l = len(candidate)
    return candidate[random_int(l)]


if __name__ == "__main__":
    print(random_int(512))
