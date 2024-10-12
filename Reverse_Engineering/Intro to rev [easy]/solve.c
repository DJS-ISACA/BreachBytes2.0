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
