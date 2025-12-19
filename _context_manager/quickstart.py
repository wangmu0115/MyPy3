with open("_httpx/quickstart.py") as fp:
    src = fp.read(60)
print(len(src))
print(fp)
print(fp.closed)
print(fp.encoding)
print(fp.read(60))

