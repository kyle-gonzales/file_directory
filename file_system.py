from tree_ import Tree
from file_descriptor import File_Descriptor
from node_ import File_Node, Folder_Node
import re
import copy as deepcopy

class File_System:
    def __init__(self) -> None:
        self.file_system = Tree(Folder_Node("root"))
        self.abs_path = ["root"]
        self.pwd = self.file_system

    def start(self):
        run = True

        while run:
            print()
            you = "You@YourPC"
            inp = input(
                f"{you} {self.print_pwd()}\n$ "
            )  # TODO: format self.abs_path from list to string

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
                    print("usage: cp source_file/source_directory target_file/target_directory")
                except ValueError as e:
                    print(
                        f"cp: failed to move {files[0]} to {files[1]}"
                    )
            elif cmd == ">":
                pass
            elif cmd == ">>":
                pass
            elif cmd == "rm":
                pass
            elif cmd == "edit":
                pass
            elif cmd == "rn":
                pass
            elif cmd == "mv":
                pass
            elif cmd == "show":
                pass
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
            curr = self.file_system
            folder_list = folder.split("/")
            new_folder = folder_list[-1]
            curr = self.traverse_node_list(folder_list[2:-1])

            self.valid_append(new_folder, curr)

            # print(self.file_system)

        elif "/" in folder and folder[0] != "/":  # relative path
            folder_list = folder.split("/")
            new_folder = folder_list[-1]
            curr = self.traverse_node_list(folder_list[:-1], self.pwd)

            self.valid_append(new_folder, curr)
            # print("relative path")
            # print(self.file_system)

        else:  # add folder in pwd
            self.valid_append(folder, self.pwd)
            # print(self.file_system)

    def valid_append(self, new_folder, curr):
        try:

            if not curr.has_child(new_folder):
                if isinstance(new_folder, str):
                    curr.append_child(Tree(Folder_Node(new_folder)))
                elif isinstance(new_folder, Tree):
                    curr.append_child(new_folder)
            else:
                raise NameError
        except NameError:
            print(f"mkdir: {new_folder}: Already exists")
        finally:
            return

    def delete_dir(self, folder: str):
        if folder[0:5] == "/root":  # absolute path
            curr = self.file_system
            folder_list = folder.split("/")
            curr = self.traverse_node_list(folder_list[2:])

            curr.parent.delete_child(curr.name.item)
            # print("relative path")
            # print(self.file_system)

        elif "/" in folder and folder[0] != "/":  # relative path
            folder_list = folder.split("/")
            curr = self.traverse_node_list(folder_list, self.pwd)
            curr.parent.delete_child(curr.name.item)
            # print("relative path")
            # print(self.file_system)

        else:  # delete folder in pwd
            if self.pwd.has_child(folder):
                self.pwd.delete_child(folder)
            else:
                raise ValueError
            # print(self.file_system)

    def navigate_(self, folder: str):  # TODO : update self.pwd and self.abs_path
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

    def create_file(self):
        pass

    def edit_file(self):
        pass

    def delete_file(self):
        pass

    def rename_file(self, path, new_name):
        pass

    """Moves a file from one directory to another. If the target directory is non-existent. It RENAMES the current directory to the new name
    """

    def move_file(self, file, path):
        pass

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
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_name
            self.valid_append(copy, copy_path)
        elif "/" in copy_ and copy_[0] != "/":  # relative path
            copy_list = copy_.split("/")
            copy_path = self.traverse_node_list(copy_list[:-1], self.pwd)
            copy_name = copy_list[-1]
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_name
            self.valid_append(copy, copy_path)
        else:  # add folder in pwd
            copy = deepcopy.deepcopy(file)
            copy.name.item = copy_
            self.valid_append(copy, self.pwd)


    def display_(self, folder: None):
        target = self.pwd.children
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
                    print(f.name.item)  # f.name prints folder_name/
        else:
            for f in target:
                print(f.name.item)

    def show_contents(self, file):
        pass

    def search_paths(self, file):
        pass

    """ 
    helper functions
    """

    def parse_input(self, inp: str):
        inp_list = inp.split()

        cmd = inp_list[0]
        files = inp_list[1:]
        # for index, f in enumerate(files): #!remove this
        #     f = f.replace(".", "\.")
        #     f = f.replace("*", ".*")
        #     f = f.replace("?", ".")
        #     files[index] = f

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

    def get_absolute_path(self):
        pass

    def split_path(self):
        pass
