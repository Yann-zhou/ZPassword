import hashlib
a = "message".encode()
print(hashlib.sha256(a).hexdigest())