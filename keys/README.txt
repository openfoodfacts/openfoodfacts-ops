# Keys and passwords

Appart from ssh public keys,
this directory contains also contains
initial password for your user on each server where it was created.

It is encrypted with your ssh public key.
So to decrypt a password, use:
```bash
openssl pkeyutl -decrypt -inkey ~/.ssh/KEY_NAME -in keys/YOUR_NAME/SERVER_NAME-password.txt
```