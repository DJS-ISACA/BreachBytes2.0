# [rev] recursion

## How it works?

The program reads flag via `stdin` and checks that its of valid length ( = 30 chars ).

Then it proceeds to validate the content by passing the start pointe and end pointer to a recursive function.

```c
int validate_chars(char *start, char *end, size_t i) {
  if (start > end) {
    return 1;
  }
  return *start == FIRST_HALF[i] && *end == SECOND_HALF[i] &&
         validate_chars(start + 1, end - 1, i + 1);
}
```

So from this information, its safe to conclude that `FIRST_HALF` contains the first half of the flag in forward order, and `SECOND_HALF` contains the second half of the flag in reverse order.



## Solution

- `FIRST_HALF` is at offset 0x3060 in the ELF and

- `SECOND_HALF` is at offset 0x30e0 in the ELF

What we can do is write a simple C program to read the ELF at these offsets and initialise the `FIRST_HALF` and `SECOND_HALF` to exactly what they were in the original program:

```c
  int fd = open("./recursion", O_RDONLY);
  pread(fd, &FIRST_HALF, sizeof(FIRST_HALF), 0x3060);
  pread(fd, &SECOND_HALF, sizeof(SECOND_HALF), 0x30e0);
  close(fd);
```

then we can simply print them in forward and backward order respectively to get the flag:

```c
  for (int i = 0; i < 15; i++) {
    printf("%c", (char)FIRST_HALF[i]);
  }
  for (int i = 14; i >= 0; i--) {
    printf("%c", (char)SECOND_HALF[i]);
  }
```

## Flag

`DJSISACA{3L!X!R--->D4RK3L!X!R}`


