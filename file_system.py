from tree_ import Tree
from file_descriptor import File_Descriptor
from node_ import File_Node, Folder_Node
import re


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
                    print(
                        f"cd: failed to change directory to {files[0]}: No such file or directory"
                    )
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
            head = self.pwd

            folder_list = folder.split("/")
            new_folder = folder_list[-1]

            curr = self.traverse_node_list(folder_list[:-1], head)

            self.valid_append(new_folder, curr)
            # print("relative path")
            # print(self.file_system)

        else:  # add folder in pwd
            self.valid_append(folder, self.pwd)

            # print(self.file_system)
    
    def valid_append(self, new_folder, curr):
            try:
                if not curr.has_child(new_folder):
                    curr.append_child(Tree(Folder_Node(new_folder)))
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
            head = self.pwd

            folder_list = folder.split("/")

            curr = self.traverse_node_list(folder_list, head)
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

    def copy_(self):
        pass

    def display_(self, folder: None | str):
        target = self.pwd.children
        if bool(folder):
            if folder == "/":
                target = self.file_system.children
            elif folder == "..":
                target = self.pwd.parent.children
            elif folder[0:5] == "/root":
                folder_list = folder.split("/")
                target = self.traverse_node_list(folder_list[2:]).children
            elif "/" in folder:
                folder_list = folder.split("/")
                target = self.traverse_node_list(folder_list, self.pwd).children
            else:
                target = self.traverse_node_list([folder], self.pwd).children

        for f in target:
            print(f.name.item)  # f.name prints folder_name/

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
        # for index, f in enumerate(files):
        #     files[index] = f.replace(".", "\.")
        #     files[index] = f.replace("*", ".*")

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

    def get_parent(self, current: Tree):
        if not current.parent:
            raise ValueError
        return current.parent

    def get_absolute_path(self):
        pass

    def split_path(self):
        pass
