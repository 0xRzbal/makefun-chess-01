import gzip, base64
src = open('engine.py', 'rb').read()
comp = gzip.compress(src)
enc = base64.b85encode(comp).decode()
payload = "import gzip,base64,os,sys,urllib.request\nexec(gzip.decompress(base64.b85decode(" + repr(enc) + ")).decode())"
open('main.py', 'w').write(payload)
print('main.py bytes:', len(payload.encode()))
