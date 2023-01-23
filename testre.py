import re

regex = '?cs*'
regex = regex.replace(".", "\.")
regex = regex.replace("*", ".*")
regex = regex.replace("?", ".")
print(regex)

r = re.compile(regex)

res = r.fullmatch("cs123f")
print(res.group(0) if res else "")