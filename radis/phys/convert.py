# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:49:43 2015

@author: Erwan

Conversion formulas between different units (works with numpy arrays)

Checks the order of magnitudes to help detect conversion errors (comparing with
standard order of magnitudes in plasma physics)

Examples of use
--------

Get equivalent width in nm of a 10cm-1 width at 380 nm
    
    >>> from radis import * 
    >>> dcm2dnm(10, nm2cm(380))

"""

from __future__ import absolute_import, division, unicode_literals
from __future__ import print_function
import numpy as np
from radis.phys.constants import eV, h, c, k_b
from radis.phys.units import conv2       # to import it from .conv if it feels more natural

# %% Energy units


def J2eV(E):
    'J to eV'
    return E / eV


def J2K(E):
    'J to Kelvin'
    return E / k_b


def J2cm(E):
    'J to cm-1'
    return E / (h * c) / 100


def eV2J(E):
    'eV to J'
    _asserteV(E)
    return E * eV
    
def eV2nm(E):
    'nm to eV'
    _asserteV(E)
    return 1/E * 1e9 * (h * c) / eV

def eV2K(E):
    'eV to K'
    _asserteV(E)
    return E * eV / k_b


def eV2cm(E):
    'eV to cm'
    _asserteV(E)
    return E * eV / (h * c) / 100


def K2eV(E):
    'eV to K'
    _assertK(E)
    return E * k_b / eV


def K2J(E):
    'Kelvin to J'
    _assertK(E)
    return E * k_b


def cm2J(E):
    'cm-1 to J'
    _assertcm(E)
    return (E * 100) * (h * c)


def cm2eV(E):
    'cm-1 to eV'
    _assertcm(E)
    return (E * 100) * (h * c) / eV


# %% Wavelength, wavenumbers and frequencies

def cm2nm(wl_cm1):
    'cm-1 to (vacuum) nm'
    return 1 / wl_cm1 * 1e9 / 100

def nm2cm(wl_nm):
    '(vacuum) nm to cm-1'
    return 1 / wl_nm * 1e9 / 100
    
def nm2eV(wl_nm):
    'nm to eV'
    return 1 / wl_nm * 1e9 * (h * c) / eV

def hz2nm(f_Hz):
    ''' frequency to wavelength
    f in Hz, output in nm '''
    return c*1e9/f_Hz

def nm2hz(lbd_nm):
    ''' wavelength to frequency 
    lbd in Hz, output in nm '''
    return c*1e9/lbd_nm

# Convert Broadenings

def dcm2dnm(delta_nu, nu_0):
    ''' Converts (ex: FWHM) from Δcm to Δnm
    
    Input
    ---
    
    delta_nu: cm-1
        wavenumber broadening
    
    nu_0: cm-1
        center wavenumber
    '''
    return cm2nm(nu_0-delta_nu/2)-cm2nm(nu_0+delta_nu/2)

def dnm2dcm(delta_lbd, lbd_0):
    ''' Converts (ex: FWHM) from Δnm to Δcm
    
    Input
    ---
    
    delta_lbd: nm
        wavelength broadening
    
    lbd_0: nm
        center wavelength
    '''
    return nm2cm(lbd_0-delta_lbd/2)-nm2cm(lbd_0+delta_lbd/2)

def dhz2dnm(deltaf_hz, f_0):
    ''' Converts (ex: FWHM) from ΔHz to Δnm
    
    Input
    ---
    
    deltaf_hz: Hz
        frequency broadening
    
    nu_0: Hz
        center frequency
    '''
    return hz2nm(f_0-deltaf_hz/2)-hz2nm(f_0+deltaf_hz/2)

def dnm2dhz(delta_lbd, lbd_0):
    ''' Converts (ex: FWHM) from Δnm to Δhz
    
    Input
    ---
    
    delta_lbd: nm
        wavelength broadening
    
    lbd_0: nm
        center wavelength
    '''
    return nm2hz(lbd_0-delta_lbd/2)-nm2hz(lbd_0+delta_lbd/2)


# %% Pressure units


def torr2bar(p_torr):
    ' Torr to bar'
    return p_torr / 1.01325 / 760


def torr2atm(p_atm):
    return p_atm / 760


def bar2torr(p_bar):
    return p_bar * 1.01325 * 760


def bar2atm(p_bar):
    return p_bar / 1.01325


def atm2torr(p_atm):
    return p_atm * 760


def atm2bar(p_atm):
    return p_atm * 1.01325

# %% Assert functions


def _magn(x):
    return np.round((np.log10(np.abs(x))))


def _assertK(E):
    try:
        m = _magn(E)
        assert(((0 <= m) & (m <= 6)).all())
    except AssertionError:
        print(('Warning. Input values may not be in Kelvin', E, 'K?'))


def _assertcm(E):
    try:
        m = _magn(E)
        assert(((2 <= m) & (m <= 5)).all())
    except AssertionError:
        print(('Warning. Input values may not be in cm-1', E, 'cm-1?'))


def _asserteV(E):
    try:
        m = _magn(E)
        assert(((0 <= m) & (m <= 2)).all())
    except AssertionError:
        print(('Warning. Input values may not be in eV', E, 'eV?'))

# %% Test


def _test(verbose=True, *args, **kwargs):
    btest = True

    E = np.linspace(1, 5, 5)  # eV
    btest *= (J2eV(K2J(J2K(eV2J(E)))) == E).all()

    E = 2150  # cm-1
    btest *= J2cm(cm2J(E))

    E = 1  # eV
    btest *= (eV2cm(E) == J2cm(eV2J(1)))
    btest *= (round(eV2K(E), 0) == 11605)
    
    E = 250 # nm
    btest *= np.isclose(nm2eV(E),cm2eV(nm2cm(E)))
    btest *= (eV2nm(nm2eV(E))==E)

    fwhm = 1.5 # nm
    lbd_0 = 632.8 # nm
    btest *= (np.isclose(fwhm, dcm2dnm(dnm2dcm(fwhm, lbd_0), nm2cm(lbd_0))))

    fwhm = 2e-3  # nm
    lbd_0 = 632.8
    fwhm_hz = dnm2dhz(fwhm, lbd_0)
    print(('{0:.2g} nm broadening at {1} nm = {2:.2g} Ghz'.format(fwhm, lbd_0, fwhm_hz*1e-9)))
    btest *= np.isclose(fwhm_hz*1e-9, 1.4973307983125002)

    return bool(btest)

if __name__ == '__main__':
    print(('Test :', _test()))
