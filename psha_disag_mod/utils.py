""" Module of simple and useful functions """
import os
import typing
from typing import List

from psha_disag_mod.compartiment import read_psha_params


def extract_poes_value(poes_name: str, sep: str = "-") -> float:
    """Extract the value of the Probability of exceedence column's name
    of Openquake's csv ouputs

    Args:
        poes_name (str): Name of the column

    Returns:
        float: Value of the Probablity of exceedence
    """

    if sep == "-":
        return float(poes_name.split(sep)[1])
    elif sep == "~":
        return float(poes_name.split(sep)[0])


def equivalent_frequency(type_acc: str) -> float:
    """Corresponding frequency from the given type of threshold acceleration

    Args:
        type_acc (str): Name of the threshold acceleration

    Returns:
        float: Frequency in Hz
    """
    if type_acc == "PGA":
        return 100
    else:
        val = 1 / float(type_acc.split("SA(")[1].split(")")[0])
        return val


def extract_frequency(column_name: str) -> float:
    """Extract from column name : the equivalent frequency of type_acc

    Args:
        column_name (str): Structure of the column "{poes}~{type_acc}". Ex : 0.0001~PGA

    Returns:
        float: Frequency in Hz
    """
    type_acc = column_name.split("~")[1]
    freq = equivalent_frequency(type_acc)
    return freq


def sorting_per_type_acc(filenames: List[str]) -> List[str]:
    """Sort the list of filenames in function of the order of threshold of acceleration

    Args:
        filenames (List[str]): list of filenames with each type of threshold of acceleration mentionned

    Returns:
        List[str]: Lsit of filenames sorted
    """
    types_acc = [
        "PGA",
        "SA(0.03)",
        "SA(0.05)",
        "SA(0.1)",
        "SA(0.15)",
        "SA(0.2)",
        "SA(0.25)",
        "SA(0.3)",
        "SA(0.4)",
        "SA(0.5)",
        "SA(0.75)",
        "SA(1.0)",
        "SA(1.5)",
        "SA(2.0)",
        "SA(3.0)",
    ]
    sorted_list = []
    assert len(filenames) == len(set(filenames))  # If duplicates --> Error
    for type_acc in types_acc:
        for filename in set(filenames):
            params_dic = read_psha_params(filename)
            type_acc_file = params_dic["type_acc"]
            if type_acc_file == type_acc:
                sorted_list.append(filename)
    return sorted_list


def seed_value(folder_output: str) -> int:
    one_filename = os.listdir(folder_output)[0]
    val = int(one_filename.split(".csv")[0].split("_")[-1])
    return val
