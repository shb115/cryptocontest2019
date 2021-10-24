from __future__ import print_function
from random import randint
from sys import argv, stdout
import collections
import random


def mulInv(n, q):  
    return extEuclid(n, q)[0] % q

def extEuclid(a, b):
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
        pass
    return s0, t0, a

def sqrRoot(n, q):
    r = pow(n,(q+1)/4,q)
    return r, q - r

Point = collections.namedtuple("Point", ["x", "y"])

class EC(object):
    def __init__(self, a, b, q):
        assert 0 < a and a < q and 0 < b and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        self.zero = Point(0, 0)
        pass

    def isOn(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r

    def findY(self, x):
        y2 = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrRoot(y2, self.q)
        return y2 == y*y%self.q, y

    def negation(self, p):
        return Point(p.x, -p.y % self.q)

    def addition(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            return self.zero
        if p1.x == p2.x:
            l = (3 * p1.x * p1.x + self.a) * mulInv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * mulInv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Point(x, y)

    def smul(self, p, n):
        r = self.zero
        m2 = p
        while 0 < n:
            if n & 1 == 1:
                r = self.addition(r, m2)
                pass
            n, m2 = n >> 1, self.addition(m2, m2)
            pass
        return r

    def random(self, xin):
        while True:
            if xin == 0 :
                x = random.randint(1,self.q)
            else :
                x = xin
            y2 = (x ** 3 + self.a * x + self.b) % self.q
            if pow(y2,(self.q-1)/2,self.q) != 1 :
                continue
            y, my = sqrRoot(y2, self.q)
            return Point(x, y)


class STREAM():
    def __init__(self, ec, seed, P, Q):
        self.ec = ec
        self.seed = seed
        self.P = P
        self.Q = Q

    def genStream(self):
        t = self.seed
        s = (self.ec.smul(self.P,t)).x
        self.seed = s
        #print("s*Q.x",hex(self.ec.smul(self.Q,s).x))
        r = (self.ec.smul(self.Q,s)).x
        return r & (2**(8 * 30) - 1)  # return 30 bytes

    def encryption(self, pt):
        loop = (len(pt)+29)/30
        ct = bytearray('')
        for i in range(0,loop):
            r = self.genStream()
            #print("r=",hex(r))
            blkLen = len(pt[30*i:30*(i+1)])
            for j in range(1,blkLen+1):
                ct += chr(((r>>((30-j)*8))&0xff)^pt[30*i+j-1])
        return ct

    def decryption(self, pt):
        return self.encryption(pt)


if __name__ == "__main__":
    prime = 112817876910624391112586233842848268584935393852332056135638763933471640076719
    A = 49606376303929463253586154769489869489108883753251757521607397128446713725753
    B = 79746959374671415610195463996521688925529471350164217787900499181173830926217
    
    ec = EC(A,B,prime)

    P = Point(103039657693294116462834651854367833897272806854412839639851017006923575559024,
              77619251402197618012332577948300478225863306465872072566919796455982120391100)
    Q = Point(54754931428196528902595765731417656438047316294230479980073352787194748472682,
               31061354882773147087028928252065932953521048346447896605357202055562579555845)

    print("P = ",P)
    print("Q = ",Q)
    print("Is on EC : ", ec.isOn(P))
    print("Is on EC : ", ec.isOn(Q))

    def num_to_str(num):
        a=''
        while(num !=0):
            a += chr(num & 0xff)
            num = num >> 8
        a = a[::-1]
        return a

    def str_to_num(abc):
        num=0
        a = [ord(i) for i in abc]
        for i in a:
            num = (num << 8) + i
        return num 
    
    pt =0xa92d66711f9ff86cd94c84d338bd983949fa3b3881d535b2e230fb338e91c2a2d17bdf6566ae6c65838b91e9b0dc3fbadcf8f03e4a18e9adeaa91f139a8fc9ef233471d50599d43fd02b511d438970ed88207e5611bba2345acf7bb42dfcfe4005a0e01a5acbedfcc100e170470c34c66fd2cc8773aa9d16e13380793363c618f83a0ef785a794d6037d7b318e54c1853b1b0e83dad3cde2b97d3ac0e918475b1e23a9e9d13388522d391050f3ecca5d47558a0935c3be1b0ff00b418475571133b94e5c14146453e9b4961635329ba8b49940baa6b9525f58d969e8b570fc7f1e2cdee17c4980b662556d564bc2975f158f067e8d3b4560538adc3bb5f02f77071cd6471dbd3b6de27a484f9688089e66e457767ee0ed12798f549ea05e6459ca11deec74986a5e3fc1444401ae7675a8c1af26ed36d341772203e8502098deb0fc7d0c322de615ea937351232a22014cde072bab7131bdf0142445241d237652fd6299c07f4adf4fa913d08558c4b81a95beccc5219934ae6f90303e1c822c4c314e7d0b9c28d364a285d165d2ba06ad1e16da5713d6cb7e15abe582ac892608b46da43642bf64a245412338c3e2409b8c23f359174c48683691d5135a043a595a919df211ea0064e7e6c5a56ba4b51aaa8e3e40141e9999d003cf468e02a2039a929cff446b3c1e8de665af665be959232297e5ed023c968d235d9505f05b25a2f55173a24c2b3f4028c0464d360b28db72d9fd652f74dde2abf501a05b54b9a9e1ed75d4e5c7fda00543aca3d8393e255c93abb411c8e2a914cce95a458eb72433a3c93ae5916cc6bfde89bf99db915d8925cb70143d88b55f36090780ca8a59e6ba385eb616ad43c6f728ecc98b136cdc14abbb5bd09f1118e84c8ab30343a1018d2cc54213269a848df366855895a6d6ea17248c3797647b91f7c94c69b6ff5c6e81cdea6a4aa1189fd998ad5ba4ea238f0589ad005cf2c6b4347dd202ea339ca3bd46afc0dd60bd13c5390e30852cf846a697f65cc450d1eb956b2e7a8e45b8b784d4f13a21e88b981d6bea9c34b089f501e58ade1483198c64698ed3d9a56af36bfa527ba544b80be5d637a204ccc8f8118d8b266675ab4326017fd83136e4aa3da93901ba544f2ebff443f5f4932179d69f88426713ec368504584df692311065e885da91a621f5f6e29cda60816f0249745958509c034d180954132897a1d978c245030131f7363d077bcec93e28cdc48769d95b5563976c76799d5159f7bf3da2ce8130863b8b0a8e0fe34b0ccf6c3f7835604a84f0462585eff39fed6f5d2d49ca87b24f3fbae4
    pt=num_to_str(pt)
    print(pt)
    
    stream = STREAM(ec,0x71e3e7d3fac11617c282d57c4ab211e2,P,Q);
    ct = stream.encryption(bytearray(pt))
    print("ct:",bytes(ct))
    
    
    stream = STREAM(ec,0xffffffffffffffff,P,Q);
    pt = stream.decryption(ct)
    print("pt:",pt)

    
    
