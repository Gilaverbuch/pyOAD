# pyoad
Python package to read .D binary data format from the Ocean Acoustic and Signals Lab (OASL) at Woods Hole Oceanographic Institution (WHOI).

In a conda environment run:
- conda install python 
- pip install build (A simple, correct PEP 517 build frontend. It will build the .whl and .tar.gz for the pip install)

Dependencies:

- Numpy
- Matplotlib
- Jupyter Notebook
- Pandas
- Xarray
- Obspy
- tqdm

** pip install should install them automatically.

To install run:

- python -m build
- pip install dist/the_desired_version.whl
