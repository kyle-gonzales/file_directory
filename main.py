from tree_ import Tree
from node_ import File_Node, Folder_Node
from file_descriptor import File_Descriptor, parse_file_name
from file_system import File_System

def main():
    """ #!Testing the tree
    t = Tree("root")
    t.insert_child("one")
    two = t.insert_child("two")
    two.insert_child("two-1").insert_child("two-1-1")
    two_2 = two.insert_child("two-2")
    two.insert_child("two-3")
    t.insert_child("three").parent.insert_child("four")

    print(t)

    print(t.has_child("three"))
    print(t.has_child(two))
    print(t.has_child(two_2))
    print(t.has_child("five"))

    two_new = t.delete_child(two)

    print(t)
    f = File_Descriptor("ts")

    print(f)
    print(repr(f))

    folder = Folder_Node(f)
    print(folder)
    print(repr(folder))

    f_tree = Tree(folder)
    t.append_child(f_tree)
    t.append_child(two_new)

    print(t)

    print(t.find_descendant_by_name("two"))
    """

    fs = File_System()
    fs.start()


if __name__ == "__main__":
    main()
