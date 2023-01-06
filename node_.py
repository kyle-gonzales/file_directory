from file_descriptor import File_Descriptor


class Node:

    def __init__(self, item, children) -> None:
        self.item = item
        self.children = children

    def __str__(self):
        return f"{self.item}"

class File_Node (Node):
    
    def __init__(self, item : File_Descriptor) -> None:
        super().__init__(item, None)

    def __repr__(self) -> str:
        return f"{self.item.name}.{self.item.extension}"

    def __str__(self) -> str:
        return f"{self.item.name}.{self.item.extension}"
        

class Folder_Node(Node):

    def __init__(self, item : File_Descriptor, children : list[Node]) -> None:
        super().__init__(item, children)
    
    def __repr__(self) -> str:
        return f"{self.item.name}/"
    def __str__(self) -> str:
        return f"{self.item.name}/"



        