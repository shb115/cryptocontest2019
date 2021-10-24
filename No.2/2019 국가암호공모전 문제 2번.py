import sys
import datetime

name=['Alice', 'almas', 'angle', 'asuka', 'balor', 'bay', 'becky', 'bobby', 'bray', 'car', 'cena', 'charl', 'cien', 'dean', 'EC3', 'edge', 'GO', 'HHH', 'kairi', 'kane', 'kurt', 'LANA', 'Natty', 'queen', 'roman', 'Ronda', 'Rusev', 'seth', 'shine', 'top', 'vega', 'vince'] 


def asc(s):
    result = 0
    for i in range(0, len(s)):
        result = (result << 8) + ord(s[i])

    return result

def mul(a, b):  # a*b
    mod = sum(1 << i for i in [40, 23, 21, 18, 16, 15, 13, 12, 8, 5, 3, 1, 0])

    result=0
    for i in range(40):
        if a & 1:
            result = result ^ b

        a = a >> 1
        b = b << 1

        if b & (1 << 40):
            b = b ^ mod

    return result

def div(a, b):
    if a < b :
        a, b = b, a
        
    q = 0
    len_a, len_b = int.bit_length(a), int.bit_length(b)
    while len_a >= len_b :
        length = len_a - len_b
        #print(len_a, len_b)
        q = q + (1 << length)
        a = a ^ (b << length)
        len_a = int.bit_length(a)
        
    return q, a

def e_gcd(a,b):
    if a > b :
        r1, r2 = a, b
    else:
        r1, r2 = b, a

    t1, t2 = 0, 1
    while r2 > 0:
        q, r = div(r1, r2)
        r1, r2 = r2, r
        t = t1 ^ mul(q, t2)
        t1, t2 = t2, t
    return t1

ID_1 = 'charl'
ID_2 = 'GO'
ASC_ID_1 = asc(ID_1)
ASC_ID_2 = asc(ID_2)

P1 = 0x51462bdbbe
C1 = 0xc59aced47d
P2 = 0xa7d618494e
C2 = 0x330afd468d

K = P1 ^ P2

fx = 0x10000A5B12B
ASC_ID = ASC_ID_1 ^ ASC_ID_2
inv_ASC_ID = e_gcd(ASC_ID, fx)

print(mul(ASC_ID, inv_ASC_ID) == 1)

Km = mul(K, inv_ASC_ID)

print(hex(Km))

k1 = mul(Km,ASC_ID_1)
k2 = mul(Km,ASC_ID_2)
print(K == k1 ^ k2)
