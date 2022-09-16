# pyoad
Python package to read .D binary data format from the Ocean Acoustic and Signals Lab (OASL) at Woods Hole Oceanographic Institution (WHOI). The package reads data in different binary formats and store is as an Obspy Trace or Stream object. These objects allow to easily process the data based on Obspy functionalities. For more information please check https://docs.obspy.org/ . The data is finally saved as miniSEED (subset of Standard for the Exchange of Earthquake Data (SEED)) that is widely used in seismology and infrasound research.

In a conda environment run:

- conda install python 

- pip install build (A simple, correct PEP 517 build frontend. It will build the .whl and .tar.gz for the pip install)

cd to the package directory and run:

- python -m build

- pip install dist/the_desired_version.whl


Dependencies:

- Numpy
- Matplotlib
- Jupyter Notebook
- Pandas
- Xarray
- Obspy
- tqdm

** pip install should install them automatically.


Example notebooks can be found in https://github.com/Gilaverbuch/pyoad-notebooks


