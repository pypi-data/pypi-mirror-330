import math
import numpy as np
from .coefficients import read_coefficients
from .calculator import calculate_geomagnetic

class WMMv2:
    def __init__(self, coeff_file=None):
        # Allow the user to pass a custom coefficients file path.
        self.coeff_file = coeff_file

        self.maxdeg = 12
        self.maxord = self.maxdeg
        self.defaultDate = 2025.0

        # Magnetic field outputs (nT and degrees)
        self.dec = 0.0   # declination
        self.dip = 0.0   # dip angle
        self.ti = 0.0    # total intensity
        self.bx = 0.0    # north intensity
        self.by = 0.0    # east intensity
        self.bz = 0.0    # vertical intensity
        self.bh = 0.0    # horizontal intensity

        # Epoch and caching variables (for geodetic conversion)
        self.epoch = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

        # WGS-84/IAU constants
        self.a = 6378.137
        self.b = 6356.7523142
        self.re = 6371.2
        self.a2 = self.a * self.a
        self.b2 = self.b * self.b
        self.c2 = self.a2 - self.b2
        self.a4 = self.a2 * self.a2
        self.b4 = self.b2 * self.b2
        self.c4 = self.a4 - self.b4

        # Allocate arrays
        self.c    = [[0.0 for _ in range(13)] for _ in range(13)]
        self.cd   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.tc   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.dp   = [[0.0 for _ in range(13)] for _ in range(13)]
        self.snorm = np.zeros(169)  # 13x13 = 169 entries
        self.sp   = np.zeros(13)
        self.cp   = np.zeros(13)
        self.fn   = np.zeros(13)
        self.fm   = np.zeros(13)
        self.pp   = np.zeros(13)
        self.k    = [[0.0 for _ in range(13)] for _ in range(13)]

        # Variables for geodetic-to-spherical conversion
        self.ct = 0.0
        self.st = 0.0
        self.r  = 0.0
        self.d  = 0.0
        self.ca = 0.0
        self.sa = 0.0

        self.start()

    def read_coefficients(self):
        read_coefficients(self)

    def start(self):
        self.maxord = self.maxdeg
        self.sp[0] = 0.0
        self.cp[0] = self.snorm[0] = self.pp[0] = 1.0
        self.dp[0][0] = 0.0

        # Read coefficients (this will use self.coeff_file if it was provided)
        self.read_coefficients()

        # Schmidt normalization factors
        self.snorm[0] = 1.0
        n = 1
        while n <= self.maxord:
            self.snorm[n] = self.snorm[n - 1] * (2 * n - 1) / n
            j = 2
            m = 0
            D1 = 1
            D2 = (n - m + D1) / D1
            while D2 > 0:
                self.k[m][n] = float(((n - 1)**2 - m**2)) / float((2 * n - 1) * (2 * n - 3))
                if m > 0:
                    flnmj = ((n - m + 1) * j) / float(n + m)
                    self.snorm[n + m * 13] = self.snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                    j = 1
                    self.c[n][m - 1] = self.snorm[n + m * 13] * self.c[n][m - 1]
                    self.cd[n][m - 1] = self.snorm[n + m * 13] * self.cd[n][m - 1]
                self.c[m][n] = self.snorm[n + m * 13] * self.c[m][n]
                self.cd[m][n] = self.snorm[n + m * 13] * self.cd[m][n]
                D2 = D2 - 1
                m = m + D1
            self.fn[n] = n + 1
            self.fm[n] = n
            n = n + 1
        self.k[1][1] = 0.0
        self.otime = self.oalt = self.olat = self.olon = -1000.0

    def get_declination(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.dec

    def get_dip_angle(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.dip

    def get_intensity(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.ti

    def get_horizontal_intensity(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bh

    def get_north_intensity(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bx

    def get_east_intensity(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.by

    def get_vertical_intensity(self, dLat, dLong, year, altitude):
        calculate_geomagnetic(self, dLat, dLong, year, altitude)
        return self.bz
