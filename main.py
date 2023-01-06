from tree_ import Tree

def main():
    t = Tree("root")
    t.insert_("one")
    two = t.insert_("two")
    two.insert_("two-1").insert_("two-1-1")
    two_2 = two.insert_("two-2")
    two.insert_("two-3")
    t.insert_("three").parent.insert_("four")

    print(t)

    print(t.has_child("three"))
    print(t.has_child(two))
    print(t.has_child(two_2))
    print(t.has_child("five"))


if __name__ == "__main__":
    main()
