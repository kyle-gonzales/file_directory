import re

""" Payload of Node. Contains the file information. Wrapped in Node
"""
class File_Descriptor:
    def __init__(self, name) -> None:
        self.name, self.extension = parse_file_name(name)

    def __repr__(self) -> str:
        return f"file_name = {self.name}\nextension = {self.extension}"

    def __str__(self) -> str:
        return f"{self.name}{self.extension if self.extension else ''}"


def parse_file_name(name):
    regex_file_name = r"^(.*?)(\.[^.]*)?$"  # folders will have an extension of None

    m = re.match(regex_file_name, name)
    # print(m.group(1,2))
    return m.group(1, 2)


"""
regex for file name
r'^([^\\]*)\.(\w+)$'
    * cannot handle '.git' or '.git'
r'^(.*?)(\.[^.]*)?$'
    * accepts 'git.' and '.git'

file paths and file name
r'((?:[^/]*/)*)(.*)'
    * does not separate file extension
r'^(.*\/)(.*?)(\.[^.]*)?$'
    * separates file extension
    * accepts 'git.' and '.git'


https://www.programiz.com/python-programming/examples/file-name-from-file-path
"""
