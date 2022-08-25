""" Module to organizeand sort the output files into specificied lists"""
import os
import re
import sys
import typing
from typing import List, Tuple, Optional


def read_psha_params(filename: str) -> Tuple[str, str, str, Optional[str], int]:
    startname, types, seed_str = filename.split(".csv")[0].split("_")
    split_types = types.split("-")

    type_acc = None
    if "uhs" not in types:
        type_acc = split_types.pop()

    if "rlz" in types:
        type_data = "-".join(split_types[1:])
    else:
        type_data = split_types[-1]

    type_filename = split_types[0]

    return {
        "startname": startname,
        "type_filename": type_filename,
        "type_data": type_data,
        "type_acc": type_acc,
        "seed": int(seed_str),
    }


def filter_filenames_psha(filenames: List[str], **kwargs):
    """Filter the content of the list of filenames to match the given pattern(s)

    Args:
        filenames (List[str]): List of all the filenames

    Kwargs:
        startname (List(str), optional): 'quantile' or 'hazard' string or None. Defaults to None.
        type_filename (List[str], optional): Name of type of file : 'curve' or 'uhs' or None. Defaults to None.
        type_data (_type_, optional): Type of data concerned :
            'mean' or '0.5' or '0.05' or '0.95' or None. Defaults to None.
        type_acc (List[str], optional): Type of acceleration threshold :
            "PGA" or "SA(0.03)" or "SA(0.05)" or "SA(0.1)" or "SA(0.15)" or
            "SA(0.2)" or "SA(0.25)" or "SA(0.3)" or "SA(0.4)" or "SA(0.5)" or "SA(0.75)" or
            "SA(1.0)" or "SA(1.5)" or "SA(2.0)" or "SA(3.0)" or None. Defaults to None.
        seed (List[int], optional): Number of the seed (Be careful : Try to have one type of seed in your folder -> Advice for the plots).
            Defaults to None.

    Returns:
        List[str]: filtered list of filenames which match with the given pattern(s)
    """

    def match(param, value):
        param_options = kwargs.get(param)
        if param_options is None:
            return True
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value in param_options
        return any(param_option in value for param_option in param_options)

    def filter_psha(filename):
        return all(
            match(param, value) for param, value in read_psha_params(filename).items()
        )

    return list(filter(filter_psha, filenames))


def filter_filenames_dis(filenames: List[str], disaggregation_patterns: List[str]):
    def filter_dis(filename):
        print(
            filename,
            disaggregation_patterns,
            [pattern in filename for pattern in disaggregation_patterns],
        )
        return all(pattern in filename for pattern in disaggregation_patterns)

    return list(filter(filter_dis, filenames))


def filter_filenames(filenames: List[str], calculation_mode: str, **kwargs):
    if calculation_mode == "psha":
        psha_filenames = filter(
            lambda filename: filename.startswith("hazard")
            or filename.startswith("quantile"),
            filenames,
        )
        return filter_filenames_psha(psha_filenames, **kwargs)
    if calculation_mode == "disaggregation":
        dis_filenames = filter(
            lambda filename: filename.startswith("Mag")
            or filename.startswith("Dist")
            or filename.startswith("Lon")
            or filename.startswith("TRT"),
            filenames,
        )
        dis_pat = kwargs.get("disaggregation_patterns", [])
        return filter_filenames_dis(dis_filenames, dis_pat)
