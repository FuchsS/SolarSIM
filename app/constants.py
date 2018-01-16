# -*- coding: utf-8 -*-
import numpy as np

AU   = 1.49598023 * 10**11             # astronomical unit: length of the semi-major axis [m]
HOUR = 3600
DAY  = 86400                           # mean solar day [s]
YEAR = 365.25                          # a solar year is a circulation of the earth on its orbit around the sun or the time required for it [days]
S    = 1367                            # so called solar constant at a distance of 1 AU [W/m²]
LATS = np.arange(-90,  90+1,  1)
#LATS = np.arange(-90,  90+1, 30)
DAYS = np.arange(  0, 366+1,  1)