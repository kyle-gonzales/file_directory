from file_descriptor import File_Descriptor
import re
from dataclasses import dataclass, field

""" Payload of Tree class. Template class for File_Node and Folder_Node
"""
@dataclass
class Node:
    item : any

    def __str__(self):
        return f"{self.item}"

"""Payload of File_System. Specialization of Node. Wraps the File_Descriptor 
"""
class File_Node(Node):
    def __init__(self, item : File_Descriptor) -> None:
        return super().__init__(item)

    def __repr__(self) -> str:
        return repr(self.item)

    def __str__(self) -> str:
        return str(self.item)


class Folder_Node(Node):
    def __init__(self, item : File_Descriptor) -> None:
        return super().__init__(item)

    def __repr__(self) -> str:
        return repr(self.item)

    def __str__(self) -> str:
        return f"{self.item}/"




