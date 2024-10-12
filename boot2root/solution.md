# [boot2root]

- `rustscan -a IP` will reveal SSH is open at port 22 and another service is open at 3000
- directly using ssh to connect doesn't work because we don't have the password (and username)
- if we use `nc` to connect to port 3000 we will be able to observe that its an HTTP server
- open IP:3000 in browser and see a login form
- an unpriviledged user's creds are leaked in source code `user:pass@123`
- logging in with that user informs that we need to login as `admin` to continue
- there is a helpful forgot password page which lets us reset the password for any user
- there is also a client side check which ensures that admin password cannot be reset
- however that can be bypassed by manually sending the request with curl, or sending an edited request with firefox, burp etc
- once we get the confirmation, we can login as admin and see a file read portal
- using that portal we can inspect the source code of the web app and see that no sanitisation is done on input, which means we can use this to traverse directory and have an arbitrary-file-read
- reading /etc/passwd tells us about a `hacker` user who uses /bin/bash as their default shell
- next idea is to read their .bash_history
- reading that we find that they created an ssh key pair and added the public key to authorized keys
- this means we can read the `id_rsa` and use that to ssh into `hacker@IP` without their password
- reading flag.txt tells us that we need to find the root password
- one way is to priv esc and read /etc/shadow and try to crack it with rockyou (fails)
- other way is to keep looking and find a `.todo.txt` file which hints at, suspicious setuid bit on `cp` and some `convention.txt` file
- use can (ab)use setuid bit `cp` to read /etc/shadow and obtain the root hash
- next we find `convention.txt` in `/opt`
- the convention says that the root password should be : `root<6_digit_number>toor`
- so we create a custom wordlist with all possible 6 digit numbers and bruteforce it
- finally we obtain the root password and the flag which is `root600065toor`

## Flag

`DJSISACA{root600065toor}`
