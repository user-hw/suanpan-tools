# python lzstring读取文件和现有库缺少的函数

lzstring是一种加密压缩和解压的工具，最早的是用JS写的

官网链接： https://pieroxy.net/blog/pages/lz-string/index.html

这次使用python的lzstring库发现网上相关的教程很少，一般只有一个示例

```python
import lzstring
 
ic = {"name": "root", "password": "123456"}
 
x = lzstring.LZString()
compressed = x.compressToBase64(str(ic))
print(compressed)
decompressed = x.decompressFromBase64(compressed)
print(decompressed)
```

```python
N4cgdghgtgpiBcACEAnA9mgLiANMgDhAM5EDuaKAJgsgIwBMAzACwCsAbCAL5A==
{'name': 'root', 'password': '123456'}
```

这段代码作者：https://blog.csdn.net/xc_zhou/article/details/106454951

但是并没有发现读取文件的相关教程，只能自己来写

```python
#解压现有的文件
import lzstring


x = lzstring.LZString()
test_path = 'test'
with open(test_path,'rb') as file:  #注意这里要用二进制进行读取
    f = file.read()
compressed = x.compressToBase64(f)
print(compressed)
```

但是由于不知道我现在的文件是用哪种加密方式的加密的，多次实验发现并不能得到我们想要的结果。

通过查看源码发现，python提供了三种解压的方法decompressFromUTF16，decompressFromBase64，decompressFromEncodedURIComponent，但是似乎都不是我们需要的。

```python
@staticmethod
def decompressFromUTF16(compressed):
    if compressed is None:
        return ""
    if compressed == "":
        return None
    return _decompress(len(compressed), 16384, lambda index: compressed[index] - 32)

@staticmethod
def decompressFromBase64(compressed):
    if compressed is None:
        return ""
    if compressed == "":
        return None
    return _decompress(len(compressed), 32, lambda index: getBaseValue(keyStrBase64, compressed[index]))

@staticmethod
def decompressFromEncodedURIComponent(compressed):
    if compressed is None:
        return ""
    if compressed == "":
        return None
    compressed = compressed.replace(" ", "+")
    return _decompress(len(compressed), 32, lambda index: getBaseValue(keyStrUriSafe, compressed[index]))

```

再次查看JS版本的lzstring的官网发现，还有compressToUint8Array，decompressFromUint8Array这一方法

```javascript
var string = "This is my compression test.";
alert("Size of sample is: " + string.length);
var compressed = LZString.compressToUint8Array(string);
alert("Size of compressed sample is: " + compressed.length);
string = LZString.decompressFromUint8Array(compressed);
alert("Sample is: " + string);
```

但是查看python版本的里面并没有，那只好参考JS版本的函数定义方法自己写一个

```javascript
//js源码的decompressFromUint8Array函数
var f = String.fromCharCode;
//decompress from uint8array (UCS-2 big endian format)
decompressFromUint8Array:function (compressed) {
    if (compressed===null || compressed===undefined){
        return LZString.decompress(compressed);
    } else {
        var buf=new Array(compressed.length/2); // 2 bytes per character
        for (var i=0, TotalLen=buf.length; i<TotalLen; i++) {
            buf[i]=compressed[i*2]*256+compressed[i*2+1];
        }

        var result = [];
        buf.forEach(function (c) {
            result.push(f(c));
        });
        return LZString.decompress(result.join(''));
    }
},
```

自己写一个进行解压

```python
import lzstring


x = lzstring.LZString()
test_path = 'test'
with open(test_path,'rb') as file:  #注意这里要用二进制进行读取
    f = file.read()

buf=[]
for i in range(len(f)//2):
    buf.append((f[i*2]*256+f[i*2+1]))
res = []
for i in buf:
    res.append(chr(i & 0xffff))
print(x.decompress(''.join(res)))
```

最后果然成功了，然后我整理了一下源代码的文件，给库的作者提交了一个函数，但是我看这个库已经是多年前写的了，不知道作者还在不在维护，但是写出一个博客和大家一起分享。