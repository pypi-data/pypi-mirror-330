# raw_bcrypt
"Raw" bcrypt, which returns bytes suitable for use as cryptographic keys.
## Usage

```py
import raw_bcrypt, secrets
raw_bcrypt.bcrypt(9, secrets.token_bytes(16), b"hunter42")
```