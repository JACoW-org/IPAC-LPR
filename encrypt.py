import crypto
import sys
sys.modules['Crypto'] = crypto

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
import base64
import hashlib
import urllib.parse


bs=AES.block_size

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    
data = _pad('Nicolas Delerue;adcdefadcdefadcdefadcdefadcdefadcdefadcdefadcdefadcdef;')

#key = get_random_bytes(16)
key = pad(b'IPAC23LightPeerReview!',16)

iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted_text=urllib.parse.quote_from_bytes(base64.b64encode(iv + cipher.encrypt(data.encode())),safe='')
#encrypted_text=base64.b64encode(iv + cipher.encrypt(data.encode()))
print("data",data)
print("key",base64.b64encode(key))
print('encrypted_text',encrypted_text)

enc = base64.b64decode(urllib.parse.unquote_to_bytes(encrypted_text))
iv = enc[:AES.block_size]
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(enc[AES.block_size:]).decode('utf-8'))

print("http://nicolas.delerue.org/ipac23/referee_acceptance_form.php?r="+encrypted_text)

exit()
    
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

print("data",data)
print(ciphertext)
print(key)

cipher = AES.new(key, AES.MODE_EAX, cipher.nonce)
decrypt_data = cipher.decrypt_and_verify(ciphertext, tag)
print(decrypt_data)
