#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uint64_t constants[] = {'}', 'G', 'n', 'I', 'R', 'e', 'E', 'N', 'i', 'g',
                        'n', 'e', '_', 'E', '5', 'r', 'E', 'V', 'e', 'r',
                        '_', '0', '7', '_', '0', 'r', '7', 'N', 'I', '{',
                        'A', 'C', 'A', 'S', 'I', 'S', 'J', 'D'};

char *super_secure_encode(char *s) {
  char *rev = (char *)malloc(sizeof(char) * strlen(s));
  int start = 0;
  int end = strlen(s) - 1;
  while (end != -1) {
    rev[start] = s[end];
    start++;
    end--;
  }
  return rev;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <FLAG>", argv[0]);
    return EXIT_FAILURE;
  }
  if (strlen(argv[1]) == 0) {
    puts("THATS EMPTY!");
    return EXIT_FAILURE;
  }
  char *rev = super_secure_encode(argv[1]);
  if (strlen(rev) != (sizeof(constants) / sizeof(constants[0]))) {
    puts("WRONG FLAG!");
    return EXIT_FAILURE;
  }
  for (int i = 0; i < strlen(rev); i++) {
    if (rev[i] != constants[i]) {
      puts("WRONG FLAG!");
      return EXIT_FAILURE;
    }
  }
  puts("GG THAT WAS CORRECT!");
  free(rev);
  return EXIT_SUCCESS;
}
