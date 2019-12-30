def check_is_ascii(s):
    return all(ord(c) < 128 for c in s)
