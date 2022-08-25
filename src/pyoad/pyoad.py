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
from .input.input import read_header, read_waveforms


def read_data(file_name):
    '''
    This function teads the data from a .D 24 bit binary file


    parameters
    ----------
        file_name: path to file

    Returns
    -------
    Header structure containing the parameters names and values



    '''


    
    Header = read_header(file_name)
    Waveforms = read_waveforms(file_name, Header)


    # samp_freq = Header['rhfs']
    # dt = 1/samp_freq
    # time = np.arange(0, len(Waveforms)*dt, dt)

    # plt.figure(figsize = (15,5))
    # plt.plot(time, Waveforms, 'g')
    # plt.xlabel('Time [sec')
    # plt.ylabel('Pressure []')
    # plt.title('SHRU waveforms')
    # plt.show()


    # f, t, Sxx = signal.spectrogram(Waveforms, samp_freq, nperseg=int(samp_freq), noverlap=int(samp_freq//2))
    # plt.figure(figsize=(10,5))
    # plt.pcolormesh(t, f, np.log10(Sxx), shading='gouraud')
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # # plt.xlim(10,20)
    # plt.ylim(0,200)
    # # plt.clim(-10, -5)
    # plt.colorbar()
    # plt.xlabel('Time [sec')
    # plt.ylabel('Frequency [Hz]')
    # plt.show()


    return Header, Waveforms

