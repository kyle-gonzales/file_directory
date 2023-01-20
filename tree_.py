from node_ import *
import re

class Tree:
    def __init__(self, name: Node, parent: "Tree" = None) -> None:

        if not name or not str(name).strip():
            raise NameError("Name must be a non-empty string")
        else:
            self.name = name
        self.parent = parent
        self.children: list[Tree] = []

    """only searches within the root node's direct children
    """

    def has_child(self, needle):
        # input can be a tree or string
        if isinstance(needle, Tree):
            return needle in self.children
        for child in self.children:
            if child.name.item == needle:
                return True
        return False

    def insert_child(self, name: Node):  # deprecated
        child = Tree(name, self)

        self.children.append(child)

        return child

    def delete_child(self, needle):  # only a parent can remove its children
        removedNode: Node
        if not self.has_child(needle):
            return
        if isinstance(needle, Tree):
            removedNode = self.children.pop(self.children.index(needle))
        else:
            for child in self.children:
                if child.name.item == needle:
                    removedNode = self.children.pop(self.children.index(child))

        if removedNode:
            removedNode.parent = None

        return removedNode

    def append_child(self, child: "Tree"):
        if not isinstance(child, Tree):
            return

        if child == self:  # avoid circular dependencies
            raise Exception("Child cannot be the parent of itself")

        parent = self.parent
        while parent != None:  # avoid circular dependencies
            if child == self:
                raise Exception("Child cannot be the parent of its ancestors")
            parent = parent.parent

        child.parent = self
        self.children.append(child)

    def print_tree(self, tree: "Tree", space_count=0):
        s = "\n"

        for child in tree.children:
            s += f"{' ' * space_count}|_{child.name}{self.print_tree(child, space_count = space_count + 2)}"

        return s

    """
    uses depth-first search to look for a descendant within the root node
    """

    def find_descendant_by_name(self, name):
        # regex = re.compile(name)
        for child in self.children:
            # match_ = regex.fullmatch(child.name.item)
            if child.name.item == name:
                return child
            child.find_descendant_by_name(name)
        return None

    def find_all_descendants_by_name(self, name): # TODO: support regex
        children = []
        regex = re.compile(name)
        for child in self.children:
            match_ = regex.fullmatch(child.name.item)
            if child.name.item == name:
                children.append(child)
            child.find_all_descendants_by_name(name)
        return children

    # deprecated
    def __traverse(self, fun):  # input is a lambda
        for child in self.children:
            if fun(child):
                return fun(child)
            child.__traverse(fun)

    def __str__(self) -> str:
        s = str(self.name)
        return s + self.print_tree(self, 2)
