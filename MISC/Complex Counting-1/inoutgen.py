import random

def binaryExponetiation(a, b, mod):
    answer = 1
    a %= mod
    while b > 0:
        if b % 2 == 1:
            answer = (answer * a) % mod
        a = (a * a) % mod
        b //= 2
    return answer

def getAnswer(n):
    answer = binaryExponetiation(2, n, mod)
    answer = (answer + (binaryExponetiation(2, n / 5, mod) * 4) % mod) % mod
    answer = (answer * binaryExponetiation(5, mod - 2, mod)) % mod
    return answer

t = 10**5
answer = 0
mod = 10**9 + 7
with open(f"InputHard.txt", "w") as file:
    file.write(str(t))
    file.write("\n")

    for _ in range(t):

        n = 1
        while n % 5 > 0:
            n = random.randint(1, 10**18 + 1)

        answer = (answer + getAnswer(n)) % mod

        file.write(str(n) + " ")

with open(f"OutputHard.txt", "w") as file:
    file.write(str(answer))