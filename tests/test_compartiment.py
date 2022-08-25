from typing import List, Dict

import pytest
import pytest_check as check

from psha_disag_mod.compartiment import read_psha_params, filter_filenames


def generate_filename(startname, type_filename, type_data, type_acc, seed):
    if type_filename == "uhs":
        type_acc = None
    types_str = "-".join(
        [t for t in (type_filename, type_data, type_acc) if t is not None]
    )
    filename = f"{startname}_{types_str}_{seed}.csv"
    params = {
        "startname": startname,
        "type_filename": type_filename,
        "type_data": type_data,
        "type_acc": type_acc,
        "seed": seed,
    }
    return filename, params


def generate_filenames(
    startnames: List[str],
    type_filenames: List[str],
    type_datas: Dict[str, List[str]],
    type_accs: List[str],
    seeds: List[int],
):
    filenames = []
    params = []
    for startname in startnames:
        for type_filename in type_filenames:
            for type_data in type_datas[startname]:
                for seed in seeds:
                    for type_acc in type_accs:
                        filename, param = generate_filename(
                            startname, type_filename, type_data, type_acc, seed
                        )
                        filenames.append(filename)
                        params.append(param)
    return filenames, params


def test_read_psha_params():
    filenames, expected_params = generate_filenames(
        startnames=("hazard", "quantile"),
        type_filenames=("uhs", "curve"),
        type_datas={
            "hazard": ["mean", "rlz-001", "rlz-002"],
            "quantile": ["0.5", "0.05", "0.95"],
        },
        type_accs=["PGA", "SA(0.1)", "SA(0.2)"],
        seeds=[0, 14, 42],
    )
    for i, filename in enumerate(filenames):
        params = read_psha_params(filename)
        check.equal(params, expected_params[i])


class TestCompartimentation:
    @pytest.fixture(autouse=True)
    def setup(self):
        """"""
        self.filenames, self.params = generate_filenames(
            startnames=("hazard", "quantile"),
            type_filenames=("uhs", "curve"),
            type_datas={
                "hazard": ["mean", "rlz-001", "rlz-002"],
                "quantile": ["0.5", "0.05", "0.95"],
            },
            type_accs=["PGA", "SA(0.1)", "SA(0.2)"],
            seeds=[0, 14, 42],
        )
        disag_filenames = [
            "TRT-0_14.csv",
            "Mag-0_14.csv",
            "Mag_Lon_Lat-0_14.csv",
            "Mag_Dist-0_14.csv",
            "Mag_Dist_Eps-0_14.csv",
            "Lon_Lat-0_14.csv",
            "Lon_Lat_TRT-0_14.csv",
            "Dist-0_14.csv",
        ]
        self.filenames.extend(disag_filenames)

    def test_empty(self):
        expected_filtered = []
        filtered = filter_filenames([], "psha")
        check.equal(filtered, expected_filtered)

    def test_all(self):
        expected_filtered = [
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_curve-mean-PGA_0.csv",
            "hazard_curve-mean-SA(0.1)_0.csv",
            "hazard_curve-mean-SA(0.2)_0.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "hazard_curve-mean-PGA_42.csv",
            "hazard_curve-mean-SA(0.1)_42.csv",
            "hazard_curve-mean-SA(0.2)_42.csv",
            "hazard_curve-rlz-001-PGA_0.csv",
            "hazard_curve-rlz-001-SA(0.1)_0.csv",
            "hazard_curve-rlz-001-SA(0.2)_0.csv",
            "hazard_curve-rlz-001-PGA_14.csv",
            "hazard_curve-rlz-001-SA(0.1)_14.csv",
            "hazard_curve-rlz-001-SA(0.2)_14.csv",
            "hazard_curve-rlz-001-PGA_42.csv",
            "hazard_curve-rlz-001-SA(0.1)_42.csv",
            "hazard_curve-rlz-001-SA(0.2)_42.csv",
            "hazard_curve-rlz-002-PGA_0.csv",
            "hazard_curve-rlz-002-SA(0.1)_0.csv",
            "hazard_curve-rlz-002-SA(0.2)_0.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-SA(0.1)_14.csv",
            "hazard_curve-rlz-002-SA(0.2)_14.csv",
            "hazard_curve-rlz-002-PGA_42.csv",
            "hazard_curve-rlz-002-SA(0.1)_42.csv",
            "hazard_curve-rlz-002-SA(0.2)_42.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_42.csv",
            "quantile_uhs-0.95_42.csv",
            "quantile_uhs-0.95_42.csv",
            "quantile_curve-0.5-PGA_0.csv",
            "quantile_curve-0.5-SA(0.1)_0.csv",
            "quantile_curve-0.5-SA(0.2)_0.csv",
            "quantile_curve-0.5-PGA_14.csv",
            "quantile_curve-0.5-SA(0.1)_14.csv",
            "quantile_curve-0.5-SA(0.2)_14.csv",
            "quantile_curve-0.5-PGA_42.csv",
            "quantile_curve-0.5-SA(0.1)_42.csv",
            "quantile_curve-0.5-SA(0.2)_42.csv",
            "quantile_curve-0.05-PGA_0.csv",
            "quantile_curve-0.05-SA(0.1)_0.csv",
            "quantile_curve-0.05-SA(0.2)_0.csv",
            "quantile_curve-0.05-PGA_14.csv",
            "quantile_curve-0.05-SA(0.1)_14.csv",
            "quantile_curve-0.05-SA(0.2)_14.csv",
            "quantile_curve-0.05-PGA_42.csv",
            "quantile_curve-0.05-SA(0.1)_42.csv",
            "quantile_curve-0.05-SA(0.2)_42.csv",
            "quantile_curve-0.95-PGA_0.csv",
            "quantile_curve-0.95-SA(0.1)_0.csv",
            "quantile_curve-0.95-SA(0.2)_0.csv",
            "quantile_curve-0.95-PGA_14.csv",
            "quantile_curve-0.95-SA(0.1)_14.csv",
            "quantile_curve-0.95-SA(0.2)_14.csv",
            "quantile_curve-0.95-PGA_42.csv",
            "quantile_curve-0.95-SA(0.1)_42.csv",
            "quantile_curve-0.95-SA(0.2)_42.csv",
        ]

        filtered = filter_filenames(self.filenames, "psha")

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_psha_curve_complex(self):
        expected_filtered = [
            "hazard_curve-mean-SA(0.2)_14.csv",
            "quantile_curve-0.5-SA(0.2)_14.csv",
            "quantile_curve-0.05-SA(0.2)_14.csv",
            "quantile_curve-0.95-SA(0.2)_14.csv",
        ]

        filtered = filter_filenames(
            self.filenames,
            "psha",
            type_filename=["curve"],
            type_data=["mean", "0.95", "0.5", "0.05"],
            type_acc=["SA(0.2)"],
            seed=[14],
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_startname(self):
        expected_filtered = [
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_curve-mean-PGA_0.csv",
            "hazard_curve-mean-SA(0.1)_0.csv",
            "hazard_curve-mean-SA(0.2)_0.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "hazard_curve-mean-PGA_42.csv",
            "hazard_curve-mean-SA(0.1)_42.csv",
            "hazard_curve-mean-SA(0.2)_42.csv",
            "hazard_curve-rlz-001-PGA_0.csv",
            "hazard_curve-rlz-001-SA(0.1)_0.csv",
            "hazard_curve-rlz-001-SA(0.2)_0.csv",
            "hazard_curve-rlz-001-PGA_14.csv",
            "hazard_curve-rlz-001-SA(0.1)_14.csv",
            "hazard_curve-rlz-001-SA(0.2)_14.csv",
            "hazard_curve-rlz-001-PGA_42.csv",
            "hazard_curve-rlz-001-SA(0.1)_42.csv",
            "hazard_curve-rlz-001-SA(0.2)_42.csv",
            "hazard_curve-rlz-002-PGA_0.csv",
            "hazard_curve-rlz-002-SA(0.1)_0.csv",
            "hazard_curve-rlz-002-SA(0.2)_0.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-SA(0.1)_14.csv",
            "hazard_curve-rlz-002-SA(0.2)_14.csv",
            "hazard_curve-rlz-002-PGA_42.csv",
            "hazard_curve-rlz-002-SA(0.1)_42.csv",
            "hazard_curve-rlz-002-SA(0.2)_42.csv",
        ]

        filtered = filter_filenames(self.filenames, "psha", startname=["hazard"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_typefilename(self):
        expected_filtered = [
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_0.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.5_42.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_0.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.05_42.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_0.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_42.csv",
            "quantile_uhs-0.95_42.csv",
            "quantile_uhs-0.95_42.csv",
        ]

        filtered = filter_filenames(self.filenames, "psha", type_filename=["uhs"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_typedata_mean(self):
        expected_filtered = [
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_0.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_uhs-mean_42.csv",
            "hazard_curve-mean-PGA_0.csv",
            "hazard_curve-mean-SA(0.1)_0.csv",
            "hazard_curve-mean-SA(0.2)_0.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "hazard_curve-mean-PGA_42.csv",
            "hazard_curve-mean-SA(0.1)_42.csv",
            "hazard_curve-mean-SA(0.2)_42.csv",
        ]

        filtered = filter_filenames(self.filenames, "psha", type_data=["mean"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_typedata_rlz(self):
        expected_filtered = [
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_curve-rlz-002-PGA_0.csv",
            "hazard_curve-rlz-002-SA(0.1)_0.csv",
            "hazard_curve-rlz-002-SA(0.2)_0.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-SA(0.1)_14.csv",
            "hazard_curve-rlz-002-SA(0.2)_14.csv",
            "hazard_curve-rlz-002-PGA_42.csv",
            "hazard_curve-rlz-002-SA(0.1)_42.csv",
            "hazard_curve-rlz-002-SA(0.2)_42.csv",
        ]
        filtered = filter_filenames(self.filenames, "psha", type_data=["rlz-002"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_typedata_allrlz(self):
        expected_filtered = [
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_0.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-001_42.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_0.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_uhs-rlz-002_42.csv",
            "hazard_curve-rlz-001-PGA_0.csv",
            "hazard_curve-rlz-001-SA(0.1)_0.csv",
            "hazard_curve-rlz-001-SA(0.2)_0.csv",
            "hazard_curve-rlz-001-PGA_14.csv",
            "hazard_curve-rlz-001-SA(0.1)_14.csv",
            "hazard_curve-rlz-001-SA(0.2)_14.csv",
            "hazard_curve-rlz-001-PGA_42.csv",
            "hazard_curve-rlz-001-SA(0.1)_42.csv",
            "hazard_curve-rlz-001-SA(0.2)_42.csv",
            "hazard_curve-rlz-002-PGA_0.csv",
            "hazard_curve-rlz-002-SA(0.1)_0.csv",
            "hazard_curve-rlz-002-SA(0.2)_0.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-SA(0.1)_14.csv",
            "hazard_curve-rlz-002-SA(0.2)_14.csv",
            "hazard_curve-rlz-002-PGA_42.csv",
            "hazard_curve-rlz-002-SA(0.1)_42.csv",
            "hazard_curve-rlz-002-SA(0.2)_42.csv",
        ]
        filtered = filter_filenames(self.filenames, "psha", type_data=["rlz-"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_type_acc(self):
        expected_filtered = [
            "hazard_curve-mean-PGA_0.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-PGA_42.csv",
            "hazard_curve-rlz-001-PGA_0.csv",
            "hazard_curve-rlz-001-PGA_14.csv",
            "hazard_curve-rlz-001-PGA_42.csv",
            "hazard_curve-rlz-002-PGA_0.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-PGA_42.csv",
            "quantile_curve-0.5-PGA_0.csv",
            "quantile_curve-0.5-PGA_14.csv",
            "quantile_curve-0.5-PGA_42.csv",
            "quantile_curve-0.05-PGA_0.csv",
            "quantile_curve-0.05-PGA_14.csv",
            "quantile_curve-0.05-PGA_42.csv",
            "quantile_curve-0.95-PGA_0.csv",
            "quantile_curve-0.95-PGA_14.csv",
            "quantile_curve-0.95-PGA_42.csv",
        ]

        filtered = filter_filenames(self.filenames, "psha", type_acc=["PGA"])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_one_pattern_seed(self):
        expected_filtered = [
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-mean_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-001_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_uhs-rlz-002_14.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "hazard_curve-rlz-001-PGA_14.csv",
            "hazard_curve-rlz-001-SA(0.1)_14.csv",
            "hazard_curve-rlz-001-SA(0.2)_14.csv",
            "hazard_curve-rlz-002-PGA_14.csv",
            "hazard_curve-rlz-002-SA(0.1)_14.csv",
            "hazard_curve-rlz-002-SA(0.2)_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.5_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.05_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_uhs-0.95_14.csv",
            "quantile_curve-0.5-PGA_14.csv",
            "quantile_curve-0.5-SA(0.1)_14.csv",
            "quantile_curve-0.5-SA(0.2)_14.csv",
            "quantile_curve-0.05-PGA_14.csv",
            "quantile_curve-0.05-SA(0.1)_14.csv",
            "quantile_curve-0.05-SA(0.2)_14.csv",
            "quantile_curve-0.95-PGA_14.csv",
            "quantile_curve-0.95-SA(0.1)_14.csv",
            "quantile_curve-0.95-SA(0.2)_14.csv",
        ]
        filtered = filter_filenames(self.filenames, "psha", seed=[14])

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_two_pattern_typefilename_typedata(self):
        expected_filtered = [
            "hazard_curve-mean-PGA_0.csv",
            "hazard_curve-mean-SA(0.1)_0.csv",
            "hazard_curve-mean-SA(0.2)_0.csv",
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "hazard_curve-mean-PGA_42.csv",
            "hazard_curve-mean-SA(0.1)_42.csv",
            "hazard_curve-mean-SA(0.2)_42.csv",
        ]

        filtered = filter_filenames(
            self.filenames, "psha", type_filename=["curve"], type_data=["mean"]
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_two_pattern_typefilenameuhs_typeaccPGA(
        self,
    ):  # 'uhs' and 'type_acc' are incompatible, so it's a combined list
        expected_filtered = []

        filtered = filter_filenames(
            self.filenames, "psha", type_filename=["uhs"], type_acc=["PGA"]
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_two_pattern_typefilename_fewtypedata(self):
        expected_filtered = [
            "hazard_curve-mean-PGA_14.csv",
            "hazard_curve-mean-SA(0.1)_14.csv",
            "hazard_curve-mean-SA(0.2)_14.csv",
            "quantile_curve-0.5-PGA_14.csv",
            "quantile_curve-0.5-SA(0.1)_14.csv",
            "quantile_curve-0.5-SA(0.2)_14.csv",
        ]

        filtered = filter_filenames(
            self.filenames,
            "psha",
            type_filename=["curve"],
            type_data=["mean", str(0.5)],
            seed=[14],
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_disag_no_pattern(self):
        expected_filtered = [
            "TRT-0_14.csv",
            "Mag-0_14.csv",
            "Mag_Lon_Lat-0_14.csv",
            "Mag_Dist-0_14.csv",
            "Mag_Dist_Eps-0_14.csv",
            "Lon_Lat-0_14.csv",
            "Lon_Lat_TRT-0_14.csv",
            "Dist-0_14.csv",
        ]

        filtered = filter_filenames(self.filenames, calculation_mode="disaggregation")

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_disag_one_pattern(self):
        expected_filtered = [
            "Mag_Dist-0_14.csv",
            "Mag_Dist_Eps-0_14.csv",
            "Dist-0_14.csv",
        ]

        disag_params = {"disaggregation_patterns": ["Dist"]}
        filtered = filter_filenames(
            self.filenames, calculation_mode="disaggregation", **disag_params
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_disag_two_pattern(self):
        expected_filtered = ["Mag_Dist-0_14.csv", "Mag_Dist_Eps-0_14.csv"]

        filtered = filter_filenames(
            self.filenames,
            calculation_mode="disaggregation",
            disaggregation_patterns=["Dist", "Mag"],
        )

        print(filtered)
        check.equal(filtered, expected_filtered)

    def test_disag_two_pincompatible_attern(self):
        expected_filtered = []

        disag_params = {"disaggregation_patterns": ["TRT", "Eps"]}
        filtered = filter_filenames(
            self.filenames, calculation_mode="disaggregation", **disag_params
        )

        print(filtered)
        check.equal(filtered, expected_filtered)
