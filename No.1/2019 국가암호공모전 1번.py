#문제에서 주어진 것
p = 4349445962213346771005425232845727838336252528805558665990590240470749947810140632785570086210529055607857683115467490199117548707954653733811730248891247
q = 50174122860490288682454191145153181183821456872777196544604225860970223720817
g = 2174582142019644155276818137638393001160821529179916986818524855155980721678000683379339584218075071275840823045973601487223201645328337396122493007683309
s1_1 = 0x19138a8168a15ec8766867e3250e61f92ce02ad33b2b6f6f9e21d63b34889165
s1_2 = 0x102c9ed2ff0fe669a36639b71869f8a3a20868f6a29a898995aef5ac43116cea
s1_3 = 0x29630c9018e65a541aa4a865c66106ec746328669841d05cb0519e8c50bfe04d
s1_5 = 0x2a7a22486cb5b0562832ca2ea4a59deb50ff8a041ca22742b20c40cab6e78688
s2_1 = 0x2811ba689e7c0c72798e0c23ea5c0676a75e7cf841c7e088835657e863374b2f
s2_4 = 0x1a5d2b618387de2e8bdc5b1a684d0153a45b0c51e2fa8a99b5d0510b58de1461
hm1 = 0x3e33f8ef50fb32f6d62734c17f074798365dbfd51c7f301e7ae11bb9d0c2af3e
hm2 = 0x2B3165E91F79AEE52E84FFD8104103E9A4CB037165972E3BD4620C74D9A259D3
hm3 = 0x441581547D29A7513A52B2121F589E8A8CCCBE945D0C45F3C9F491EC2EA5B920
hm4 = 0x5E7787E6A858F9C4843C3C4A20CBB4B362F1212C570387D32DDFEB598CCD49E8
hm5 = 0xA7192532964CD5DF41D46DAF4ED4FF8F43B75C8107428CCE75C09AD9F4E2AE15

#역원 구하는 함수
def e_gcd(a,b):
    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0,1
    while ( r2 > 0):
        q = r1//r2
        r = r1-q*r2
        r1, r2 = r2, r
        s = s1-q*s2
        s1, s2 = s2, s
        t = t1-q*t2
        t1, t2 = t2, t
    return s1

def str_to_num(abc):
    num=0
    a = [ord(i) for i in abc]
    for i in a:
        num = (num << 8) + i
    return num

def num_to_str(num):
    a=''
    while(num !=0):
        a += chr(num & 0xff)
        num = num >> 8
    a = a[::-1]
    return a

#d구하기
z = s1_1 * (s2_4 - s2_1)
s = e_gcd(z, q)
d = ((s2_1 * hm4 - s2_4 * hm1) * s) % q

#1문단,4문단 r찾기
s2_1_inverse = e_gcd(s2_1, q)
r1 = ((hm1 + d * s1_1) * s2_1_inverse) % q
print(num_to_str(r1))

s2_2_inverse = e_gcd(s2_1, q)
r2 = ((hm2 + d * s1_2) * s2_2_inverse) % q

s2_3_inverse = e_gcd(s2_1, q)
r3 = ((hm3 + d * s1_3) * s2_3_inverse) % q

s2_4_inverse = e_gcd(s2_4, q)
r4 = ((hm4 + d * s1_1) * s2_4_inverse) % q

s2_5_inverse = e_gcd(s2_1, q)
r5 = ((hm5 + d * s1_5) * s2_5_inverse) % q

#검산
k = pow(g, r1, p)
kk = k % q
print(kk == s1_1)
