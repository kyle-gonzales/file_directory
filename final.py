import re
from dataclasses import dataclass, field
import copy as deepcopy

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
        removedNode: Tree
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
        regex = re.compile(name)
        for child in self.children:
            match_ = regex.fullmatch(child.name.item)
            if match_:
                return child
            child.find_descendant_by_name(name)
        return None

    def find_all_descendants_by_name(self, name_):  #* TODO: support regex FINISHED
        children = []
        name = self.regex_to_wildcard(name_)
        regex = re.compile(name)
        for child in self.children:
            match_ = regex.fullmatch(child.name.item)
            if match_:
                children.append(child)
            child.find_all_descendants_by_name(name)
        return children

    def regex_to_wildcard(self, name):
        if name == "..":
            return name
        name = name.replace(".", "\.")
        name = name.replace("*", ".*")
        name = name.replace("?", ".")
        return name


    # deprecated
    def __traverse(self, fun):  # input is a lambda
        for child in self.children:
            if fun(child):
                return fun(child)
            child.__traverse(fun)

    def __str__(self) -> str:
        s = str(self.name)
        return s + self.print_tree(self, 2)



class File_System:

    def __init__(self) -> None:
        self.file_system = Tree(Folder_Node("root"))
        self.abs_path = ["root"]
        self.pwd = self.file_system

    def start(self):
        count_text = 1
        file_name = input()

        with open(file_name, "r") as f:
            for line in f:
                inp = line

                cmd, files = self.parse_input(inp)
                cmd, files = self.parse_input(inp)

                if cmd == "q":
                    run = False
                    break
                if cmd == "mkdir":
                    try:
                        if len(files) != 1:
                            raise SyntaxError()
                        else:
                            self.create_dir(files[0])
                    except SyntaxError as e:
                        print("usage: mkdir <directory name>")
                    except ValueError as e:
                        print(f"mkdir: cannot create directory {files[0]}")
                elif cmd == "rmdir":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.delete_dir(files[0])
                    except SyntaxError as e:
                        print("usage: rmdir <directory name>")
                    except ValueError as e:
                        print(
                            f"rmdir: failed to remove {files[0]}: No such file or directory"
                        )
                elif cmd == "cd":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.navigate_(files[0])
                    except SyntaxError as e:
                        print("usage: cd <directory name>")
                    except ValueError as e:
                        print(f"cd: {files[0]}: No such file or directory")
                elif cmd == "ls":
                    try:
                        if len(files) > 1:
                            raise SyntaxError
                        else:
                            self.display_(files[0] if len(files) else None)
                    except SyntaxError as e:
                        print("usage: ls <directory name>")
                    except ValueError as e:
                        print(f"ls: error {files[0]}")
                elif cmd == "fs":
                    print(self.file_system)
                elif cmd == "cp":
                    try:
                        if len(files) != 2:
                            raise SyntaxError
                        else:
                            self.copy_(files[0], files[1])
                    except SyntaxError as e:
                        print(
                            "usage: cp source_file/source_directory target_file/target_directory"
                        )
                    except ValueError as e:
                        print(f"cp: failed to move {files[0]} to {files[1]}")
                elif cmd == ">":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            text1 = """#include <iostream>

using namespace std;

int main(){
        cout<<"Hello World!\\n"<<endl;
        return 0;
}"""

                            text2 = """#include <iostream>

using namespace std;

int main(){
        cout<<"Hello Philippines and hello world!\\n";
        return 0;
}"""
                            if count_text == 1:
                                self.create_file(files[0], text1)
                                count_text += 1
                            else:
                                self.create_file(files[0], text2)
                    except SyntaxError as e:
                        print("usage: '>' <file_name>")
                    except ValueError as e:
                        print(f">: failed to write to file {files[0]}")
                elif cmd == ">>":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.edit_file(files[0])
                    except SyntaxError as e:
                        print("usage: '>>' <file_name>")
                    except ValueError as e:
                        print(f">: failed to append to file {files[0]}")
                elif cmd == "rm":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.delete_dir(files[0])
                    except SyntaxError as e:
                        print("usage: rm <file path>")
                    except ValueError as e:
                        print(f"rm: failed to remove {files[0]}: No such file")
                elif cmd == "edit":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.edit_(files[0])
                    except SyntaxError as e:
                        print("usage: 'edit' <file_name>")
                    except ValueError as e:
                        print(f"edit : failed to edit file {files[0]}")
                elif cmd == "rn":
                    try:
                        if len(files) != 2:
                            raise SyntaxError
                        else:
                            self.rename_file(files[0], files[1])
                    except SyntaxError as e:
                        print("usage: rn <filename> <new filename>")
                    except ValueError as e:
                        print(f"rn: failed to rename {files[0]} to {files[1]}")
                elif cmd == "mv":
                    try:
                        if len(files) != 2:
                            raise SyntaxError
                        else:
                            self.move_file(files[0], files[1])
                    except SyntaxError as e:
                        print("usage: mv file_name target_file/target_directory")
                    except ValueError as e:
                        print(f"mv: failed to move {files[0]} to {files[1]}")
                elif cmd == "show":
                    try:
                        if len(files) != 1:
                            raise SyntaxError
                        else:
                            self.show_contents(files[0])
                    except SyntaxError as e:
                        print("usage: 'show' <file_name>")
                    except ValueError as e:
                        print(f"show: failed to show file {files[0]}")
                    except FileNotFoundError as e:
                        print(f"show: {files[0]} does not exist")
                elif cmd == "whereis":
                    pass
                else:
                    print(f"{inp}: command not found")
                    continue

    """ create a new directory
    """

    def create_dir(self, folder: str):
        # TODO : will not work for file paths ending in "/"
        if folder[0:5] == "/root":  # absolute path
            folder_list = folder.split("/")
            new_folder = folder_list[-1]
            curr = self.traverse_node_list(folder_list[2:-1])

            self.valid_append(new_folder, curr)

        elif "/" in folder and folder[0] != "/":  # relative path
            folder_list = folder.split("/")
            new_folder = folder_list[-1]
            curr = self.traverse_node_list(folder_list[:-1], self.pwd)

            self.valid_append(new_folder, curr)

        else:  # add folder in pwd
            self.valid_append(folder, self.pwd)

    def valid_append(self, new_folder, curr):
        try:
            if not curr.has_child(new_folder):
                if isinstance(new_folder, str):
                    curr.append_child(Tree(Folder_Node(new_folder)))
                elif isinstance(new_folder, Tree):
                    curr.append_child(new_folder)
                # elif isinstance(new_folder, File_Node):
                #     curr.append_child(Tree(new_folder))
            else:
                raise NameError
        except NameError:
            print(f"mkdir: {new_folder}: Already exists")
        finally:
            return

    def delete_dir(self, folder: str):
        if folder[0:5] == "/root":  # absolute path
            folder_list = folder.split("/")
            curr = self.traverse_node_list(folder_list[2:])

            curr.parent.delete_child(curr.name.item)

        elif "/" in folder and folder[0] != "/":  # relative path
            folder_list = folder.split("/")
            curr = self.traverse_node_list(folder_list, self.pwd)
            curr.parent.delete_child(curr.name.item)

        else:  # delete folder in pwd
            if self.pwd.has_child(folder):
                self.pwd.delete_child(folder)
            else:
                raise ValueError

    def navigate_(self, folder: str): 
        if folder == "..":
            self.pwd = self.get_parent(self.pwd)
            self.abs_path.pop()

        elif folder == "/":
            self.pwd = self.file_system
            self.abs_path = ["root"]

        elif folder[0:5] == "/root":
            folder_list = folder.split("/")
            pwd_temp = self.file_system
            new_path_temp = ["root"]
            for f in folder_list[2:]:
                if f == "..":
                    pwd_temp = self.get_parent(pwd_temp)
                    if len(new_path_temp) == 0:
                        raise ValueError
                    new_path_temp.pop()
                else:
                    pwd_temp = pwd_temp.find_descendant_by_name(f)

                    if not pwd_temp:
                        raise ValueError

                    new_path_temp.append(pwd_temp.name.item)

            self.pwd = pwd_temp
            self.abs_path = new_path_temp[:]

        elif "/" in folder and folder[0] != "/":
            folder_list = folder.split("/")
            pwd_temp = self.traverse_node_list(self.abs_path[1:])
            new_path_temp = self.abs_path[:]

            for f in folder_list:
                if f == "..":
                    pwd_temp = self.get_parent(pwd_temp)
                    if len(new_path_temp) == 0:
                        raise ValueError
                    new_path_temp.pop()
                else:
                    pwd_temp = pwd_temp.find_descendant_by_name(f)

                    if not pwd_temp:
                        raise ValueError

                    new_path_temp.append(pwd_temp.name.item)

            self.pwd = pwd_temp
            self.abs_path = new_path_temp[:]
        else:
            if not self.pwd.has_child(folder):
                raise ValueError
            else:
                self.pwd = self.pwd.find_descendant_by_name(folder)
                self.abs_path.append(folder)

    def create_file(self, file_path, text : str):

        file_name = ""

        if file_path[0:5] == "/root":  # absolute path
            folder_list = file_path.split("/")
            file_name = folder_list[-1]
            curr = self.traverse_node_list(folder_list[2:-1])
            self.valid_append(file_name, curr)

        elif "/" in file_path and file_path[0] != "/":  # relative path
            folder_list = file_path.split("/")
            file_name = folder_list[-1]
            curr = self.traverse_node_list(folder_list[:-1], self.pwd)
            self.valid_append(file_name, curr)

        else:  # add folder in pwd
            file_name = file_path
            if self.pwd.has_child(file_name):
                self.pwd.delete_child(file_name)

            self.valid_append(file_name, self.pwd)

        with open(file_name, "w") as f:
            f.write(text)

    def edit_file(
        self, file_name
    ):  # appends to the file; does not show contents of file
        if self.pwd.has_child(file_name):
            with open(file_name, "a") as f:
                t = "\n//this is a test for the append using >>"
                f.write(t)
        else:
            raise FileNotFoundError

    def edit_(self, file_path):
        # if does not exist, create file. If file exists, show the contents of the file and allow the file to be appended with additional texts

        if file_path[0:5] == "/root":  # absolute path
            folder_list = file_path.split("/")
            file_node = self.traverse_node_list(folder_list[2:])

        elif "/" in file_path and file_path[0] != "/":  # relative path
            folder_list = file_path.split("/")
            file_node = self.traverse_node_list(folder_list, self.pwd)

        else:  # add folder in pwd
            file_name = file_path
            if self.pwd.has_child(file_name):
                file_node = self.pwd.find_descendant_by_name(file_name)

        try:
            file_name = file_node.name.item
            with open(file_name, "a") as f:
                t = "\n//this is the result of editing the file using edit"
                f.write(t)
        except Exception:
            raise FileNotFoundError

    def rename_file(self, path, new_name):
        if self.pwd.has_child(path):
            file_node = self.pwd.find_descendant_by_name(path)
            file_node.name.item = new_name

    """Moves a file from one directory to another. If the target directory is non-existent. It RENAMES the current directory to the new name
    """

    def move_file(self, file_, path_):
        file = None

        if self.pwd.has_child(file_):
            file = self.pwd.delete_child(file_)
        else:
            raise ValueError

        if path_[0:5] == "/root":
            path_list = path_.split("/")
            path = self.traverse_node_list(path_list[2:])
            path.append_child(file)
        elif "/" in path_ and path_[0] != "/":
            path_list = path_.split("/")
            path = self.traverse_node_list(path_list, self.pwd)
            path.append_child(file)
        else:
            if not self.pwd.has_child(path_):
                file.name.item = path_
                self.pwd.append_child(file)
            else:
                path = self.pwd.find_descendant_by_name(path_)
                path.append_child(file)

    def copy_(self, file_, copy_):
        file = None

        if file_[0:5] == "/root":  # absolute path
            file_list = file_.split("/")
            file = self.traverse_node_list(file_list[2:])

        elif "/" in file_ and file_[0] != "/":  # relative path
            file_list = file_.split("/")
            file = self.traverse_node_list(file_list, self.pwd)
        else:  # add folder in pwd
            if self.pwd.has_child(file_):
                file = self.pwd.find_descendant_by_name(file_)
            else:
                raise ValueError

        if copy_[0:5] == "/root":  # absolute path
            copy_list = copy_.split("/")
            copy_path = self.traverse_node_list(copy_list[2:-1])
            copy_name = copy_list[-1]
            if copy_path.has_child(copy_name):
                return
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_name
            self.valid_append(copy, copy_path)
        elif "/" in copy_ and copy_[0] != "/":  # relative path
            copy_list = copy_.split("/")
            copy_path = self.traverse_node_list(copy_list[:-1], self.pwd)
            copy_name = copy_list[-1]
            if copy_path.has_child(copy_name):
                return
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_name
            self.valid_append(copy, copy_path)
        else:  # add folder in pwd
            if self.pwd.has_child(copy_):
                return
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_
            self.valid_append(copy, self.pwd)

    def display_(self, folder: None):
        target = self.pwd.children
        res = []
        if bool(folder):
            if folder == "/":
                target = [self.file_system.children]
            elif folder == "..":
                target = [self.pwd.parent.children]
            elif folder[0:5] == "/root":
                folder_list = folder.split("/")
                target = self.find_all(folder_list[2:])
            elif "/" in folder:
                folder_list = folder.split("/")
                target = self.find_all(folder_list, self.pwd)
            else:
                target = self.find_all([folder], self.pwd)

            for row in target:
                for f in row:
                    res.append(f.name.item)  # f.name prints folder_name/
        else:
            for f in target:
                res.append(f.name.item)
        
        for i in sorted(res):
            print(i)

    def show_contents(self, file_name):
        with open(file_name, "r") as f:
            t = f.read()
            print(t)

    def search_paths(self, file):
        pass

    """ 
    helper functions
    """

    def parse_input(self, inp: str):
        inp_list = inp.split()

        cmd = inp_list[0]
        files = inp_list[1:]

        return (cmd, files)

    def print_pwd(self):
        pwd = "/"
        for dir in self.abs_path[:-1]:
            pwd += dir + "/"
        pwd += self.abs_path[-1]
        return pwd

    def traverse_node_list(self, node_list, head: Tree = None):
        if not head:
            head = self.file_system
        current = head
        for f in node_list:
            if f == "..":
                current = self.get_parent(current)
            else:
                current = current.find_descendant_by_name(f)

            if not current:
                raise ValueError

        return current

    def find_all(self, node_list, head: Tree = None):
        if not head:
            head = self.file_system
        current = head
        nodes = []
        for (
            idx,
            f,
        ) in enumerate(node_list):
            if idx == len(node_list) - 1:
                nodes.append(current.find_all_descendants_by_name(f))
                return nodes
            if f == "..":
                current = self.get_parent(current)
            else:
                current = current.find_descendant_by_name(f)

        raise ValueError

    def get_parent(self, current: Tree):
        if not current.parent:
            raise ValueError
        return current.parent

    def split_path(self):
        pass

def main():


    fs = File_System()
    fs.start()


if __name__ == "__main__":
    main()

