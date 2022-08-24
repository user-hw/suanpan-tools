import json
import lzstring




x = lzstring.LZString()

path = 'C:/Users/wudai.xhw/AppData/Local/xuelang/suanpan-desktop/data/minio/suanpan/studio/user_public/component/5587/'
unins000 = 'data'

unins_path = path+unins000

with open(unins_path,'rb') as file:
    f = file.read()

buf =['0' for i in range(len(f)//2)]

for i in range(len(f)//2):
    buf[i] = ((f[i*2]*256+f[i*2+1]))

res = []
for i in buf:
    res.append(chr(i & 0xffff))


content = x.decompress(''.join(res))
content_json = json.loads(content)


PrettyJson = json.dumps(content_json, indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
print(PrettyJson)
