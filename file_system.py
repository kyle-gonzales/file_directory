from tree_ import Tree
from file_descriptor import File_Descriptor
from node_ import File_Node, Folder_Node
import re


class File_System:
    def __init__(self) -> None:
        self.file_system = Tree(Folder_Node("root"))
        self.pwd = ["root"]

    def start(self):
        run = True

        while run:
            print()
            you = "You@YourPC"
            inp = input(f"{you} {self.pwd}\n$ ")

            cmd, files = self.parse_input(inp)

            if cmd == "q":
                run = False
                break
            if cmd == "mkdir":
                try:
                    if len(files) != 1:
                        raise ValueError()
                    else:
                        self.create_dir(files[0])
                except ValueError as e:
                    print("usage: mkdir <directory name>")
                finally:
                    continue
            else:
                print(f"{inp}: command not found")
                continue

    """ create a new directory
    """
    def create_dir(self, folder : Tree): # TODO handle absolute paths and relative paths
        child =  Tree(Folder_Node(folder))
        self.file_system.append_child(child)

    def delete_dir(self):
        pass

    def navigate_(self):
        pass

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

    def display_(self):
        pass

    def show_contents(self, file):
        pass

    def search_paths(self, file):
        pass

    """ 
    helper functions
    """

    def parse_input(self, inp : str):
        inp_list = inp.split()
        
        cmd = inp_list[0]
        files = inp_list[1:]

        return (cmd, files)

    def get_absolute_path(self):
        pass

    def split_path(self):
        pass