# [rev] unpack

## How it works?

- The program reads flag via CLI argument

- Create a memory mapping : `mmap(NULL, 97, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)`

- Calls `populate_mem` which will use XOR cipher on the 97 bytes stored in global variable `PACKED` with the key `IHOPETHISDOESNTGETLEAKED`

- This unpacked memory location is then type casted as function pointer with the following signature : `int (*check_flag)(char *) = (void *)mem;`

- Then it does the flag check via : `strlen(argv[1]) == 35 && check_flag(argv[1])`

## Solution

The unpacked bytes in that memory location are responsible for handling the flag check. To proceed further we need to dump that unpacked data:

```python
with open('./unpack', 'rb') as f:
    f.seek(0x2008)
    enc = f.read(0x61)

key = b'IHOPETHISDOESNTGETLEAKED'
code = xor(enc, key)
print(disasm(code))
```

```nasm
   0:   b8 76 33 7d 00          mov    eax, 0x7d3376
   5:   50                      push   rax
   6:   48 b8 66 72 30 6d 5f 34 62 30   movabs rax, 0x3062345f6d307266
  10:   50                      push   rax
  11:   48 b8 5f 63 30 6d 31 6e 67 5f   movabs rax, 0x5f676e316d30635f
  1b:   50                      push   rax
  1c:   48 b8 7b 64 72 34 67 30 6e 35   movabs rax, 0x356e30673472647b
  26:   50                      push   rax
  27:   48 b8 44 4a 53 49 53 41 43 41   movabs rax, 0x4143415349534a44
  31:   50                      push   rax
  32:   b9 23 00 00 00          mov    ecx, 0x23
  37:   48 89 e6                mov    rsi, rsp
  3a:   8a 1f                   mov    bl, BYTE PTR [rdi]
  3c:   38 1e                   cmp    BYTE PTR [rsi], bl
  3e:   75 16                   jne    0x56
  40:   48 ff c6                inc    rsi
  43:   48 ff c7                inc    rdi
  46:   48 ff c9                dec    rcx
  49:   48 83 f9 00             cmp    rcx, 0x0
  4d:   7f eb                   jg     0x3a
  4f:   b8 01 00 00 00          mov    eax, 0x1
  54:   eb 05                   jmp    0x5b
  56:   b8 00 00 00 00          mov    eax, 0x0
  5b:   5b                      pop    rbx
  5c:   5b                      pop    rbx
  5d:   5b                      pop    rbx
  5e:   5b                      pop    rbx
  5f:   5b                      pop    rbx
  60:   c3                      ret
```

Clearly the flag is being constructed dynamically by pushing it in 8 byte segments on the stack. Then a loop is created which validates all the user-input characters with the real flag.

1. We can use a debugger to view the constructed flag ourselves or

2. just pack those bytes manually

```python
print(p64(0x4143415349534a44).decode(), end='')
print(p64(0x356e30673472647b).decode(), end='')
print(p64(0x5f676e316d30635f).decode(), end='')
print(p64(0x3062345f6d307266).decode(), end='')
print(p64(0x7d3376).decode())
```

## Flag

`DJSISACA{dr4g0n5_c0m1ng_fr0m_4b0v3}`
