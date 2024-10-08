# [rev] time-bomb

## How it works

- This is definitely challenging

- Its a UPX packed binary so you do any sane static analysis you will need to decompress it : `$ upx -d time-bomb`

- Now its a statically linked && stripped binary. This makes the reverse engineering process a whole lot harder.

- First of all it takes input to a source file via CLI arg.

- Then it calls `init()` as per usual but calls some function and stores the result in a global variable. The result is also passed as argument into another function.

- Then it opens a file and calculates its length ( strace can be very helpful here ).

- Then it reads the file contents into a string.

- Then it calls a function which seemingly returns some garbage random bytes.

- Next it does XOR cipher on the file contents and those random bytes

- The encrypted result is then written into a `.enc` file

## Solution

The main obstacle is in realising that the random string is computed via `rand() % 0xff` with `srand(time(0))` in `init()`

This can be actually verified by printing the EPOCH timestamp along with the encrypted data:

```shell
➜  time-bomb echo "AAAABBBB" > secret.txt
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391727
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 2f2a 2e29 c703 c8c9 e128 b005 67         /*.).....(..g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391729
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 312a 7303 8f40 03e2 c14f 7705 67         1*s..@...Ow.g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391731
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 332a 06df 8559 14c4 3cc2 9905 67         3*...Y..<...g
```

Everytime we get a different encrypted result, but if we run it very fast within the same second:

```shell
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391771
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 5b2a 1a8f c7ea 8671 a4a0 9305 67         [*.....q....g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391771
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 5b2a 1a8f c7ea 8671 a4a0 9305 67         [*.....q....g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391771
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 5b2a 1a8f c7ea 8671 a4a0 9305 67         [*.....q....g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391772
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 5c2a ff86 116d d376 2513 5005 67         \*...m.v%.P.g
➜  time-bomb date +'%s' && ./time_bomb secret.txt && xxd secret.txt.enc
1728391772
[+] Saved encrypted file to 'secret.txt.enc'
00000000: 5c2a ff86 116d d376 2513 5005 67         \*...m.v%.P.g
```

You can see that the encrypted result stays the same for the same timestamp.

Furthermore, another interesting fact you can observe is this:

```shell
➜  time-bomb wc -c secret.txt*
 9 secret.txt
13 secret.txt.enc
```

The encrypted file as +4 more bytes than original

If we inspect whats happening in the write function we notice some werid implementations

- firstly the lower two bytes from the global variable initialised in `init()` (which we know to be time(0) by assumption) is written

- then the encrypted data is written

- then the upper two bytes from the timestamp is written

So in all, this encryption scheme ironically leaks the seed for the random characters which were used for encryption.

---

What we need to do is basically read the data in the same way it is written and initalise rang with the same leaked seed. Then we can generate the same key using `rand() % 0xff` and XOR it with enc contents to get back plaintext:

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

time_t SEED;

size_t get_length(FILE *fp) {
  fseek(fp, 0, SEEK_END);
  size_t ret = ftell(fp);
  rewind(fp);
  return ret;
}

int main(void) {
  FILE *fp = fopen("flag.txt.enc", "r");
  size_t length = get_length(fp);
  char *data = malloc(length - 4);
  if (data == NULL) {
    fprintf(stderr, "malloc failed\n");
    return EXIT_FAILURE;
  }
  fread(&SEED, 2, 1, fp);
  fread(data, length - 4, 1, fp);
  fread((void *)&SEED + 2, 2, 1, fp);
  srand(SEED);
  for (int i = 0; i < length - 4; i++) {
    data[i] ^= rand() % 0xff;
  }
  write(STDOUT_FILENO, data, length - 4);
  free(data);
  fclose(fp);
}
```

## Flag

`DJSISACA{YOU_TH1nk_yOU_c4N_D3stROy_Th3_B4S3}`
