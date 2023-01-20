import re

regex = '*.*'
regex = regex.replace(".", "\.")
regex = regex.replace("*", ".*")
print(regex)

r = re.compile(regex)

res = r.fullmatch("hello.hello.hello")
print(res.group(0) if res else "")