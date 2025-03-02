from rs1101 import random_string as rs


def random_mac():
    s = rs.random_string(12, rs.candidate_dict["h"])
    lst = [s[i : i + 2] for i in range(0, len(s), 2)]
    ret = ":".join(lst)
    return ret


if __name__ == "__main__":
    print(random_mac())
