from tree_ import Tree
from node_ import File_Node
from file_descriptor import File_Descriptor


def main():
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

    fi = Tree(File_Node(File_Descriptor("test", "txt")))
    t.append_child(fi)
    t.append_child(two_new)

    print(t)

    print(t.find_descendant_by_name("two"))


if __name__ == "__main__":
    main()
