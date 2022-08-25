"Module about all metadata from the job.ini (input file) of Openquake Quake"
import os
import typing
import json
from typing import Dict


def metadata_jobini(input_folder: str, filename_ini: str, delimiter: str = " ") -> Dict:
    """Extract metadata from .ini file (input file for Openquake)
    Args:
        input_folder (str): Folder path containing the .ini file
        filename_ini (str): INI Filename (ex: 'job.ini')
        delimiter (str, optional): Delimiter used in the INI file. Defaults to " ".

    Returns:
        Dict: Dictionary containing few useful metadata from the given Openquake INI file
    """

    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0

    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read(os.path.join(input_folder, filename_ini))

    metadata = {
        "geometry": {"sites": list(config.get("geometry", "sites").split(delimiter))},
        "site_params": {
            "vs30": config.getfloat("site_params", "reference_vs30_value"),
        },
        "calculation": {
            "inv_t": config.getfloat("calculation", "investigation_time"),
            "im_types_levels": json.loads(
                config.get("calculation", "intensity_measure_types_and_levels")
            ),  # Dict
            "maximum_distance": config.getfloat("calculation", "maximum_distance"),
            "pointsource_distance": config.getfloat(
                "calculation", "pointsource_distance"
            ),
            "minimum_magnitude": config.getfloat("calculation", "minimum_magnitude"),
        },
        "disaggregation": {
            "disag_poes": list(
                config.get("disaggregation", "poes_disagg").split(delimiter)
            ),
            "magbin": config.getfloat("disaggregation", "mag_bin_width"),
            "distbin": config.getfloat("disaggregation", "distance_bin_width"),
            "coordbin": config.getfloat("disaggregation", "coordinate_bin_width"),
            "eps": config.getint("disaggregation", "num_epsilon_bins"),
        },
        "output": {
            "poes": list(config.get("output", "poes").split(delimiter)),
            "type_data": list(
                config.get("output", "quantile_hazard_curves").split(delimiter)
            ),
        },
    }
    return metadata
