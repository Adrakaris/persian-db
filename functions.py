from csv import reader
from typing import List, Tuple, TypeVar

T = TypeVar('T')
Table = List[List[T]]

# functions
def read_csv(filename: str) -> Table[str]:
    """
    Reads a csv file into a 2D array
    
    :param filename: file to read
    :return: csv entries
    """
    dictionary: Table[str] = []
    with open(filename, encoding="utf-8") as fn:
        text = reader(fn, delimiter=";")
        next(text)  # skip the header
        for ln in text:
            dictionary.append(ln)
    return dictionary
    
    
def linearly_find(target_and_coln:List[Tuple[str, int]], dict:Table[str]) -> Table[str]:
    """We do not trust that this dictionary is a 1:1 mapping, so we need to get all results that match our column.
    
    Since we need to search by multiple columns, we can't sort and be efficient by searching on one key.
    
    Thus, linear search.

    Args:
        target_and_coln (List[Tuple[str, int]]): List of tuples of (target, column target is in) - columns should not exceed the last column index of the dictionary
        dict (Table[str]): The 2D array dictionary to search by

    Returns:
        Table[str]: An aggregate of all results
    """
    out_table: Table[str] = []
    for row in dict:
        for target, coln in target_and_coln:
            if row[coln] == target:
                out_table.append(row)
    return out_table