import os
from dataclasses import dataclass
from typing import List
import re


def read_file(filepath : str):
    with open(filepath, 'r') as f:
        content = f.read()
    return content


if __name__ == "__main__":
    pass