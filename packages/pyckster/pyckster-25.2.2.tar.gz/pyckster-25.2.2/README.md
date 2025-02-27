<img src="https://gitlab.in2p3.fr/metis-geophysics/pyckster/-/raw/master/images/pyckster.png?ref_type=heads" alt="pyckster" width="200"/>

[![pipeline status](https://gitlab.in2p3.fr/metis-geophysics/pyckster/badges/master/pipeline.svg)](https://gitlab.in2p3.fr/metis-geophysics/pyckster/-/commits/master) 
[![GitLab Tag](https://img.shields.io/gitlab/v/tag/metis-geophysics%2Fpyckster?gitlab_url=https%3A%2F%2Fgitlab.in2p3.fr)](https://gitlab.in2p3.fr/metis-geophysics/pyckster/-/tags)
[![PyPI - Version](https://img.shields.io/pypi/v/pyckster)](https://pypi.org/project/pyckster/)
[![PyPI Downloads](https://static.pepy.tech/badge/pyckster)](https://pepy.tech/projects/pyckster)
![PyPI - Downloads](https://img.shields.io/pypi/dm/PyCKSTER)

PyCKSTER is an open-source PyQt5-based GUI for picking seismic traveltimes. It reads seismic files in SEG2, SEGY and Seismic Unix (SU) formats. Picked traveltimes are saved in [pyGIMLi](https://www.pygimli.org)'s unified format so they can easily be inverted to reconstruct subsurface velocity models.

PyCKSTER can read SEG2, SEGY and Seismic Unix (SU) files (although SEG2 headers are not read correctly yet). You can import source and geophone elevation from csv files. You can also update headers information (ffid, source and trace coordinates, delay), and save shots with these updated headers in SEGY and SU formats.

## Installation

You can simply download the package from PyPi:
``` bash
pip install pyckster
```

Or download the sources file in the Gitlab repository and unzip it in the directory of your choice.

## Running PyCKSTER

If you installed PyCKSTER with Pypi, open a terminal and run:
```bash
pyckster
```

If you downloaded the source files, open a terminal, move to the `pyckster-master` directory and run:
```bash
python pyckster.py
```

## How to use PyCKSTER

Here is an example of PyCKSTER in action:

<img src="https://gitlab.in2p3.fr/metis-geophysics/pyckster/-/raw/master/images/screenshot_01.png?ref_type=heads"/>

More detailed instructions coming soon...

## Author
PyCKSTER is currently developped by [Sylvain Pasquet](https://orcid.org/0000-0002-3625-9212)\
[sylvain.pasquet@sorbonne-universite.fr](sylvain.pasquet@sorbonne-universite.fr)


*CNRS, Sorbonne Université*\
*UAR 3455 OSU ECCE TERRA*\
*UMR 7619 METIS*


Any feedback or help is welcome.

## Licence

PyCKSTER is distributed under the terms of the GPLv3 license. Details on
the license agreement can be found [here].

[here]: LICENCE