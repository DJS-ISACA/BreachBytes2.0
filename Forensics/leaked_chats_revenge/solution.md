# [foren] leaked chats (revenge)

## Solution

- we observe another conversation leak in the tcp port `8080`

- from the conversation it seems that this time the two users seem to be using some sort of "secure protocol" to share the flag

- analysing the network packets between the conversation, we find HTTP packets through which one of the user downloads the "protocol.rs" file

- this protocol securely uses AES256 to encrypt the flag file

- but while sending it sends the following chunk to port 1337

```
[ENCRYPTED CONTENT][NONCE][KEY]
```

- effectively leaking everything for us

- so we can dump everything on port 1337 into "protocol.dump" and write a similar script to parse the contents and decrypt the flag

- upon decryption the flag turns out to be a PNG file which contains the flag in plain-sight

## solve.rs

```rust
use std::{
    fs::{File, OpenOptions},
    io::{self, Read, Write},
};

use aes_gcm::{aead::Aead, Aes256Gcm, Key, KeyInit};

fn main() -> io::Result<()> {
    let mut file = File::open("protocol.dump")?;
    let mut contents = Vec::new();
    file.read_to_end(&mut contents)?;
    let nonce_start = contents.len() - (32 + 12);
    let key_start = contents.len() - 32;
    let enc = &contents[..nonce_start];
    let nonce = &contents[nonce_start..key_start];
    let key = &contents[key_start..];
    let key: &Key<Aes256Gcm> = key.into();
    let cipher = Aes256Gcm::new(&key);
    let plaintext = cipher.decrypt(nonce.into(), enc).unwrap();
    file = OpenOptions::new()
        .create_new(true)
        .write(true)
        .open("flag")
        .unwrap();
    file.write_all(&plaintext)?;
    Ok(())
}
```

## Flag

`DJSISACA{1_5H0ULD_H4V3_n3V3r_TrU5T3d_y0u_w1TH_my_53cr3t5}`
