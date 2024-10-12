# [REV] Intro to rev

## How it works?

- The program takes flag input via CLI argument.
- The given flag is passed to a `super_secure_encode` which ironically just reverses the flag.
- The encoded (reversed) flag is then compared byte by byte with `constants`

## Solution

- So `constants` contain the reversed bytes of the actual flag
- We can simply read them and print it in reversed order to get the actual flag
