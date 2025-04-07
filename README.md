# PwnUtils

This repo is a collection of custom pwn tools written in python to help with pwn challenges

## Usage

### cyclfind.py

Pretty much useless, does the same as cyclic -l but in the cli

```bash
$ cyclfind
Usage: find.py <string> <pattern>
Example: find.py abcde cd
```
```bash
$ cyclfind abcdef de
3
```

### paybin.py

This one is usefull, it permits to create pwn payloads very easily

```bash
$ paybin
Usage: paybin [options]
Options:
  -u <char>,<count>     : Unicode UTF-8 (repeats character)
  -b <hex>              : Bytes (e.g., '1234' becomes \x12\x34)
  -r <hex>              : Bytes in reverse order
  -bx <hex-string>      : Hex-encoded bytes (e.g., '\x12\x34')
  -rx <hex-string>      : Hex-encoded bytes in reverse order
  -o <output-file>      : Specify output file (required)
  -v                    : Verbose mode (print payload details)

Example: paybin -u A,28 -r 76910408 -o output.bin
         paybin -v -u A,28 -rx "\x76\x91\x04\x08" -o output.bin
```
```bash
$ paybin -u "A,28" -r "08049182" -u "A,4" -u "B,4" -u "C,4" -v -o payload.bin

Payload written to payload.bin (44 bytes)
Payload length: 44 bytes
Hex view: 4141414141414141414141414141414141414141414141414141414182910408414141414242424243434343
ASCII view: AAAAAAAAAAAAAAAAAAAAAAAAAAAA....AAAABBBBCCCC
Bytes view: b'\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x82\x91\x04\x08\x41\x41\x41\x41\x42\x42\x42\x42\x43\x43\x43\x43'
```

```bash
$ paybin -u "A,28" -r "08049182" -u "A,4" -r "deadbeef" -r "c0debabe" -v -o payload.bin

Payload written to payload.bin (44 bytes)
Payload length: 44 bytes
Hex view: 414141414141414141414141414141414141414141414141414141418291040841414141efbeaddebebadec0
ASCII view: AAAAAAAAAAAAAAAAAAAAAAAAAAAA....AAAA........
Bytes view: b'\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x82\x91\x04\x08\x41\x41\x41\x41\xef\xbe\xad\xde\xbe\xba\xde\xc0'
```

### addbin.py

This one is simply used to add binary files to the environement

it does the following :

- read all the files ending with .py in the current directory
- if they don't have the python shebang, add it
- make the file executable
- link it from current dir to /bin and remove the .py 

```bash
$ sudo addbin
[-] Skipped cyclfind.py
[-] Skipped addbin.py
[-] Skipped paybin.py
```

Here all the files are skipped because they are allready exported, now i have access to all the .py files everywhere in my terminal

For example it turned only directory local paybin.py to /bin/paybin which makes it available in all the directories

