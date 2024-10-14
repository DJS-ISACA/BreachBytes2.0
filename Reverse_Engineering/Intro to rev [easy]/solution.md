# [REV] Intro to rev

## How it works?

- The program takes flag input via CLI argument.
- The given flag is passed to a `super_secure_encode` which ironically just reverses the flag.
- The encoded (reversed) flag is then compared byte by byte with `constants`

## Solution

- So `constants` contain the reversed bytes of the actual flag
- We can simply read them and print it in reversed order to get the actual flag

```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

// constants start @ 0x3060 in the ELF
// and extend till (not including) 0x3190

unsigned long constants[ (0x3190-0x3060) >> 3 ];

int main(void) {
  int fd = open("./intro", O_RDONLY);
  pread(fd, constants, sizeof(constants), 0x3060);
  close(fd);
  for (int i = (sizeof(constants) >> 3)-1 ; i >= 0 ; i--) {
    printf("%c", constants[i]);
  }
  puts("");
  return 0;
}
```

## Flag

`DJSISACA{IN7r0_70_reVEr5E_engiNEeRInG}`
