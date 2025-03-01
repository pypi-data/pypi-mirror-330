import os

def read_coefficients(instance):
    """
    Read the WMM coefficients from a file.
    
    If the instance has set a custom 'coeff_file' attribute,
    that file will be used. Otherwise, the default packaged file is used.
    """
    file_path = getattr(instance, 'coeff_file', None)
    if not file_path:
        file_path = os.path.join(os.path.dirname(__file__), "data", "WMM.COF")
    with open(file_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 1:
                break
            if len(parts) == 3:
                instance.epoch = float(parts[0])
                instance.defaultDate = instance.epoch + 2.5
            else:
                n = int(parts[0])
                m = int(parts[1])
                gnm = float(parts[2])
                hnm = float(parts[3])
                dgnm = float(parts[4])
                dhnm = float(parts[5])
                if m <= n:
                    instance.c[m][n] = gnm
                    instance.cd[m][n] = dgnm
                    if m != 0:
                        instance.c[n][m - 1] = hnm
                        instance.cd[n][m - 1] = dhnm
