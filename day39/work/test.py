import os
import hmac
secret_key = b'linhaifeng bang bang bang'
msg=os.urandom(32)
h=hmac.new(secret_key,msg)
digest=h.digest()
print(digest)

print(hmac.compare_digest(b'\x11%\xb5\xbe~\x1e\xfd\x14\xd7\x06\x17\xfd\xca\xe3 \\',digest))