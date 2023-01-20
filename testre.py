import re


regex = 'abc0?.ts'
regex = regex.replace(".", "\.")
regex = regex.replace("*", ".*")
regex = regex.replace("?", ".")
print(regex)

r = re.compile(regex)

res = r.fullmatch("abc01.ts")
print(res.group(0) if res else "does not match")