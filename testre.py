import copy
# import re

# regex = '?cs*'
# regex = regex.replace(".", "\.")
# regex = regex.replace("*", ".*")
# regex = regex.replace("?", ".")
# print(regex)

# r = re.compile(regex)

# res = r.fullmatch("cs123f")
# print(res.group(0) if res else "")


class Car:
    def __init__(self, name) -> None:
        self.name = name


a =  Car("honda")
b = copy.deepcopy(a)



print(id(a))
print(a.name)
print(id(b))
print(b.name)