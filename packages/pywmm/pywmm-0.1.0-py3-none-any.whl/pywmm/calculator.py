import math

def calculate_geomagnetic(instance, fLat, fLon, year, altitude=0):
    """
    Compute the geomagnetic field components.
    This function updates the instance with the computed values.
    """
    instance.glat = fLat
    instance.glon = fLon
    instance.alt = altitude
    instance.time = year

    dt = instance.time - instance.epoch
    pi = math.pi
    dtr = pi / 180.0
    rlon = instance.glon * dtr
    rlat = instance.glat * dtr
    srlon = math.sin(rlon)
    srlat = math.sin(rlat)
    crlon = math.cos(rlon)
    crlat = math.cos(rlat)
    srlat2 = srlat * srlat
    crlat2 = crlat * crlat

    instance.sp[1] = srlon
    instance.cp[1] = crlon

    if altitude != instance.oalt or fLat != instance.olat:
        q = math.sqrt(instance.a2 - instance.c2 * srlat2)
        q1 = altitude * q
        q2 = ((q1 + instance.a2) / (q1 + instance.b2)) ** 2
        ct = srlat / math.sqrt(q2 * crlat2 + srlat2)
        st = math.sqrt(1.0 - ct * ct)
        r2 = altitude * altitude + 2.0 * q1 + (instance.a4 - instance.c4 * srlat2) / (q * q)
        r = math.sqrt(r2)
        d = math.sqrt(instance.a2 * crlat2 + instance.b2 * srlat2)
        ca = (altitude + d) / r
        sa = instance.c2 * crlat * srlat / (r * d)
        instance.ct = ct
        instance.st = st
        instance.r  = r
        instance.d  = d
        instance.ca = ca
        instance.sa = sa
    else:
        ct = instance.ct
        st = instance.st
        r  = instance.r
        d  = instance.d
        ca = instance.ca
        sa = instance.sa

    if fLon != instance.olon:
        m = 2
        while m <= instance.maxord:
            instance.sp[m] = instance.sp[1] * instance.cp[m - 1] + instance.cp[1] * instance.sp[m - 1]
            instance.cp[m] = instance.cp[1] * instance.cp[m - 1] - instance.sp[1] * instance.sp[m - 1]
            m += 1

    aor = instance.re / r
    ar = aor * aor
    br = 0.0
    bt = 0.0
    bp = 0.0
    bpp = 0.0

    n = 1
    while n <= instance.maxord:
        ar = ar * aor
        m = 0
        D1 = 1
        D2 = (n + m + D1) / D1
        while D2 > 0:
            if altitude != instance.oalt or fLat != instance.olat:
                if n == m:
                    instance.snorm[n + m * 13] = st * instance.snorm[n - 1 + (m - 1) * 13]
                    instance.dp[m][n] = st * instance.dp[m - 1][n - 1] + ct * instance.snorm[n - 1 + (m - 1) * 13]
                if n == 1 and m == 0:
                    instance.snorm[n + m * 13] = ct * instance.snorm[n - 1 + m * 13]
                    instance.dp[m][n] = ct * instance.dp[m][n - 1] - st * instance.snorm[n - 1 + m * 13]
                if n > 1 and n != m:
                    if m > n - 2:
                        instance.snorm[n - 2 + m * 13] = 0.0
                        instance.dp[m][n - 2] = 0.0
                    instance.snorm[n + m * 13] = ct * instance.snorm[n - 1 + m * 13] - instance.k[m][n] * instance.snorm[n - 2 + m * 13]
                    instance.dp[m][n] = ct * instance.dp[m][n - 1] - st * instance.snorm[n - 1 + m * 13] - instance.k[m][n] * instance.dp[m][n - 2]
            instance.tc[m][n] = instance.c[m][n] + dt * instance.cd[m][n]
            if m != 0:
                instance.tc[n][m - 1] = instance.c[n][m - 1] + dt * instance.cd[n][m - 1]
            par = ar * instance.snorm[n + m * 13]
            if m == 0:
                temp1 = instance.tc[m][n] * instance.cp[m]
                temp2 = instance.tc[m][n] * instance.sp[m]
            else:
                temp1 = instance.tc[m][n] * instance.cp[m] + instance.tc[n][m - 1] * instance.sp[m]
                temp2 = instance.tc[m][n] * instance.sp[m] - instance.tc[n][m - 1] * instance.cp[m]
            bt = bt - ar * temp1 * instance.dp[m][n]
            bp = bp + instance.fm[m] * temp2 * par
            br = br + instance.fn[n] * temp1 * par
            if st == 0.0 and m == 1:
                if n == 1:
                    instance.pp[n] = instance.pp[n - 1]
                else:
                    instance.pp[n] = ct * instance.pp[n - 1] - instance.k[m][n] * instance.pp[n - 2]
                parp = ar * instance.pp[n]
                bpp = bpp + instance.fm[m] * temp2 * parp
            D2 -= 1
            m += 1
        n += 1

    if st == 0.0:
        bp = bpp
    else:
        bp = bp / st

    instance.bx = -bt * ca - br * sa
    instance.by = bp
    instance.bz = bt * sa - br * ca

    instance.bh = math.sqrt(instance.bx * instance.bx + instance.by * instance.by)
    instance.ti = math.sqrt(instance.bh * instance.bh + instance.bz * instance.bz)

    instance.dec = math.atan2(instance.by, instance.bx) / dtr
    instance.dip = math.atan2(instance.bz, instance.bh) / dtr

    instance.otime = instance.time
    instance.oalt = altitude
    instance.olat = fLat
    instance.olon = fLon
