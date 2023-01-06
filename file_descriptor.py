from dataclasses import dataclass


@dataclass
class File_Descriptor:
    name: str
    extension: str

#TODO: take in entire file name as string instead of individual parameters and parse the string into different groups. use regex