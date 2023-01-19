from tree_ import Tree
from file_descriptor import File_Descriptor
from node_ import File_Node, Folder_Node
import re


class File_System:
    def __init__(self) -> None:
        self.file_system = Tree(Folder_Node("root"))
        self.pwd = ["root"]
        self.current_node = self.file_system

    def start(self):
        run = True

        while run:
            print()
            you = "You@YourPC"
            inp = input(f"{you} {self.pwd}\n$ ") # TODO: format self.pwd from list to string

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
                finally:
                    continue
            elif cmd == "rmdir":
                try:
                    if len(files) != 1:
                        raise SyntaxError
                    else:
                        self.delete_dir(files[0])
                except SyntaxError as e:
                    print("usage: rmdir <directory name>")
                except ValueError as e:
                    print(f"rmdir: failed to remove {files[0]}: No such file or directory")
                finally:
                    continue
            else:
                print(f"{inp}: command not found")
                continue

    """ create a new directory
    """
    def create_dir(self, folder : str):
        # TODO : will not work for file paths ending in "/"
        if folder[0:5] == "/root":  # absolute path
            curr = self.file_system
            folder_list = folder.split("/") 
            new_folder = folder_list[-1]
            curr = self.traverse_node_list(folder_list[2:-1])
            curr.append_child(Tree(Folder_Node(new_folder)))
            print(self.file_system)

        elif "/" in folder and folder[0] != '/': # relative path
            head = self.traverse_node_list(self.pwd[1:])

            folder_list = folder.split("/") 
            new_folder = folder_list[-1]

            curr = self.traverse_node_list(folder_list[:-1], head)

            curr.append_child(Tree(Folder_Node(new_folder)))
            # print("relative path")
            print(self.file_system)
            
        else: # add folder in pwd
            child =  Tree(Folder_Node(folder))
            self.current_node.append_child(child)
            print(self.file_system)

    def delete_dir(self, folder : str):
        if folder[0:5] == "/root":  # absolute path
            curr = self.file_system
            folder_list = folder.split("/") 
            curr = self.traverse_node_list(folder_list[2:])

            curr.parent.delete_child(curr.name.item)
            # print("relative path")
            print(self.file_system)

        elif "/" in folder and folder[0] != '/': # relative path
            head = self.traverse_node_list(self.pwd[1:]) # ! refactor to self.current

            folder_list = folder.split("/") 

            curr = self.traverse_node_list(folder_list, head)
            curr.parent.delete_child(curr.name.item)
            # print("relative path")
            print(self.file_system)
            
        else: # delete folder in pwd
            if self.current_node.has_child(folder):
                self.current_node.delete_child(folder)
            else:
                raise ValueError
            print(self.file_system)

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

    def traverse_node_list(self, node_list, head : Tree = None):
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

    def get_parent(self, current : Tree):
        if not current.parent:
            raise ValueError
        return current.parent

    def get_absolute_path(self):
        pass

    def split_path(self):
        pass