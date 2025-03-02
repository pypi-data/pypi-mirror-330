from hashlib import sha3_224, sha3_256, sha3_384, sha3_512
from math import inf, log
from string import (
    ascii_letters,
    ascii_lowercase,
    ascii_uppercase,
    digits,
    printable,
    punctuation,
    whitespace,  # 6
)
from typing import List
import rs1101.random_int as ri


hexdigits = digits + ascii_letters[:6]
Hexdigits = hexdigits.upper()
candidate_dict = {
    "d": digits,  # 10
    "h": hexdigits,  # 16
    "H": Hexdigits,  # 16
    "l": ascii_lowercase,  # 26
    "u": ascii_uppercase,  # 26
    "p": punctuation,  # 32
    "i": ascii_letters + digits + punctuation,  # 26*2+10+32=94
    "a": printable,  # 100
}
cddt_default = ["u", "l", "d"]

candidate = ""
for x in cddt_default:
    candidate += candidate_dict[x]


def strength(length, clen):
    return int(log(clen**length, 2))


def random_string(length, candidate=candidate):
    ret = [ri.choice(candidate) for _ in range(length)]
    return "".join(ret)


def s2rs(s, length, candidate=candidate, deep=10):
    hashfunlst = [sha3_224, sha3_256, sha3_384, sha3_512]
    hlen = len(hashfunlst)
    prefix = "rs1101".encode("utf8")

    x = sha3_256(s.encode("utf8"))
    for _ in range(deep):
        v = int(x.hexdigest(), 16) % hlen
        hashfun = hashfunlst[v]
        x = hashfun(prefix + x.digest())
    x = int(x.hexdigest(), 16)
    ret = int2rs(x, length, candidate)

    return ret


def wash_cddt(cddt: List[str]):
    cddt = sorted(set(cddt))
    exclusive = sorted(["a", "H", "h"])
    for x in exclusive:
        if x in cddt:
            cddt = [x]
            break
    return cddt


def g_candidate(cddt):
    cddt = wash_cddt(cddt)
    candidate_lst = []
    for x in cddt:
        candidate_lst.append(candidate_dict[x])
    candidate = "".join(candidate_lst)
    return candidate


def int2rs(x, length=None, candidate=candidate):
    l = len(candidate)
    ret = []
    remain = length if length else inf
    while x > 0 and remain > 0:
        x, r = divmod(x, l)
        ret.append(candidate[r])
        remain -= 1
    if length and len(ret) < length:
        lack = length - len(ret)
        ret.append(candidate[0] * lack)
    return "".join(ret[::-1])


def rs2int(rs, candidate=candidate):
    l = len(candidate)
    ret = 0
    weight = 1
    for x in rs[::-1]:
        ret += candidate.index(x) * weight
        weight *= l
    return ret


if __name__ == "__main__":
    length = 20
    s = random_string(length)
    strength = strength(length, len(candidate))
    print(s, strength)
    print(hexdigits)
    x = rs2int(s)
    y = int2rs(x)
    assert s == y
    print(s, x, y)
    print(s2rs("嗨", 10))
    print(s2rs("嗨", 20))
