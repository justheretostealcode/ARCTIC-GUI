"""file to hold the DataStorage class"""
from dataclasses import dataclass

@dataclass
class DataStorage():
    """class to store information persistent across the program"
    """
    bool_func: str



storage = DataStorage("")
