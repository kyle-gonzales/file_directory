from file_descriptor import File_Descriptor
import re

class Node:
    def __init__(self, item, children) -> None:
        self.item = item
        self.children = children

    def __str__(self):
        return f"{self.item}"


class File_Node(Node):
    def __init__(self, item: File_Descriptor) -> None:
        super().__init__(item, None)

    def __repr__(self) -> str:
        return f"{self.item.name}.{self.item.extension}"

    def __str__(self) -> str:
        return f"{self.item.name}.{self.item.extension}"


class Folder_Node(Node):
    def __init__(self, item: File_Descriptor, children: list[Node]) -> None:
        super().__init__(item, children)

    def __repr__(self) -> str:
        return f"{self.item.name}/"

    def __str__(self) -> str:
        return f"{self.item.name}/"

def is_valid_file_name(file_name):
    regex_file_name = r'^(.*?)(\.[^.]*)?$' 


"""
regex for file name
r'^.*\/(.*)\.?(.*)$'

file paths and file name
r'((?:[^/]*/)*)(.*)'
https://www.programiz.com/python-programming/examples/file-name-from-file-path
"""