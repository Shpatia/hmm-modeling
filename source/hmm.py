def len_nod(a, b):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return steps

def ker(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def hmm_sum(x, y):
    return int(x + y)

def hmm_mod(x, y):
    return x % y if y != 0 else 0