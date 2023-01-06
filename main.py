from tree_ import Tree

def main():
    t = Tree("root")
    t.insert_("one")
    two = t.insert_("two")
    two.insert_("two-1").insert_("two-1-1")
    two.insert_("two-3")
    t.insert_("three").parent.insert_("four")

    print(t)
if __name__ == "__main__":
    main()
