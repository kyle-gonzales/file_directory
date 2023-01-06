from node_ import *


class Tree:
    def __init__(self, name : Node, parent : "Tree" = None) -> None:

        if (not name or not name.strip()):
            raise NameError("Name must be a non-empty string")
        else:
            self.name = name
        self.parent= parent
        self.children : list[Tree] = []

    def insert_(self, name : str):
        child = Tree(name, self)

        self.children.append(child)

        return child

    def print_tree(self, tree : "Tree", space_count = 0):
        str = "\n"

        for child in tree.children:
            str += f"{' ' * space_count}{child.name}{self.print_tree(child, space_count = space_count + 2)}"

        return str
    
    def __str__(self) -> str:
        return self.print_tree(self)

