# PyWMM Package

This package computes geomagnetic field components using the World Magnetic Model (WMM).

## Usage

```python
from pywmm import WMMv2

wmm = WMMv2()
declination = wmm.get_declination(34.0, -118.0, 2025, 0)
print("Declination:", declination)
```
