# **PSHA_disag_tool**

Developed by Camille Huitorel (internship in EDF Lab R&D Paris-Saclay) - 08/2022
***
## Table of Contents
1. [General Info](#General-info)
2. [Installation](#Installation-prerequisites)
3. [License](#License)

-------------------------------------------------------------------

## General Info
The OpenQuake-Engine is a suite of open source software packages part of OpenQuake (OQ) and is an open-source hazard and risk calculation engine developed by Global Earthquake Model Foundation’s (GEM).


This tool provides:
  * The ability to filter with the given patterns and mode of calculation concerned in the whole list of files provided by OpenQuake. This function has also been unit tested.
  * Three types of visualization of OpenQuake results : seismic hazard curve, UHS (Uniform Hazard Spectrum) and disaggregation plots.

## Installation
### Recommended : create a virtual environment

```bash
python -m venv .env
```

### Install dependencies :

```bash
pip3 install -r requirements.txt
```
Note : You can use pip instead of pip3, if required.

## License
PSHA_disag_tool is licensed under the [MIT](LICENSE.TXT) license.
