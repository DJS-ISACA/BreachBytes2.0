import random as r, time as t, base64 as b64, zlib as z, hashlib as h, codecs as c

def o_0(d,k): return bytes(a^b for a,b in zip(d,k))
def o_1(l): return bytes(r.randint(0,255) for _ in range(l))
def o_2(s): return c.encode(s,'rot13')
def o_3(d): return b64.b32encode(d).decode()

def o_4(m):
    o_5 = o_2(m).encode()
    o_6, o_7 = o_1(len(o_5)), o_1(r.randint(8,16))
    o_8 = o_0(o_5, o_6)
    o_9 = o_3(o_8)
    o_10 = o_0(o_9.encode(), o_7 * (len(o_9) // len(o_7) + 1))
    o_11 = z.compress(o_10)
    o_12 = b64.b85encode(o_11).decode()
    o_13 = h.sha256(o_5 + o_6 + o_7).hexdigest()
    o_14 = ''.join(r.choice('0123456789ABCDEF') for _ in range(64))
    return o_12, o_6, o_7, o_13, o_14

print("Welcome to the Secure Encryptor v1.0")
t.sleep(r.uniform(1, 3))
m = input("Enter your message: ")
e, k1, k2, ih, vt = o_4(m)
print(f"Encrypted data: {e}")
print(f"Key 1: {','.join(map(str, k1))}")
print(f"Key 2: {','.join(map(str, k2))}")
print(f"Integrity hash: {ih}")
print(f"Verification token: {vt}")










































































#part 4: gv6fzd






































#part 2: 589h_vw9fe_

























# part 1: Y9_j9f_




























#part 3: VDX33_ 
