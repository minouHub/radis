# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:44:48 2017

@author: erwan

Constants and correlations for air 
"""


def air_index_dispersion(lbd):
    ''' Return air index dispersion as a function of wavelength 
    
    Index
    ---------
    
    lbd: µm
    
    Reference:
    ----------
    
    P. E. Ciddor. "Refractive index of air: new equations for the visible and 
    near infrared", Appl. Optics 35, 1566-1573 (1996)
    
    https://refractiveindex.info/?shelf=other&book=air&page=Ciddor
    Standard air: dry air at 15 °C, 101.325 kPa and with 450 ppm CO2 content.
    
    '''
    
    n = 1 + 0.05792105/(238.0185-lbd**-2)+0.00167917/(57.362-lbd**-2)
    
    return n 


# Wavelength medium conversion functions

def vacuum2air(wavelength):
    ''' Converts wavelength as seen in vacuum to wavelength as seen in air
    
    Input
    -----
    
    wavelength: array (nm)
    
    '''
    
    air_index = air_index_dispersion(wavelength * 1e-3)      # nm > µm
    return wavelength / air_index

def air2vacuum(wavelength):
    ''' Converts wavelength as seen in air to wavelength as seen in vacuum
    
    Input
    -----
    
    wavelength: array (nm)
    
    Note
    ---------
    
    Not exactly true, as air_index_dispersion is defined for vacuum wavelength
    However, air_index_dispersion doesnt vary much on 1-2 cm-1 (which is typical
    of air index dispersion effect on air/vacuum wavelength in the mid-IR)
    
    Test with:
        
    >>> vacuum2air(air2vacuum(w))-w
    
    '''
    
    air_index = air_index_dispersion(wavelength * 1e-3)       # nm > µm
    return air_index * wavelength
