# -*- coding: utf-8 -*-
"""
Python module to read the .D binary data files

.. module:: py ocean acoustics data

:author:
    Gil Averbuch (gil.averbuch@whoi.edu)

:copyright:
    Gil Averbuch

:license:
    This code is distributed under the terms of the
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '16'
plt.rcParams['figure.dpi'] = 125
plt.rcParams['figure.facecolor'] = 'white'

import numpy as np
import pandas as pd

from scipy import signal
from obspy import read_inventory, read, signal, UTCDateTime, Stream, Trace
from .input.input import read_header_24bit, read_waveforms_24bit


def read_data_24bit(file_name, records_range):
    '''
    This function teads the data from a .D 24 bit binary file


    parameters
    ----------
        file_name: path to file
        records_range : range of record sections to extact

    Returns
    -------
    Header structure containing the parameters names and values


    '''


    
    Header = read_header_24bit(file_name)
    Waveforms = read_waveforms_24bit(file_name, Header, records_range)




    return Header, Waveforms

