__all__ = ['cd', 'ad', 'ld', 'lookback', 'age']
from math import sqrt,sinh,sin

DH = 2997.92458 #in Mpc/h
OM = 0.3
NZ = 10000
TH = 9.77813106 #in Gyr/h

def E(z,om,ol,ok):
    zp1 = float(z) + 1.0
    return sqrt((om*zp1 + ok)*zp1*zp1 + ol)

def chi(z,om,ol,ok,Nz=NZ):
    dz = z/float(Nz)
    return sum(map(lambda i: 1.0/E(dz*i,om,ol,ok), xrange(Nz)))*dz

def dm(z,om,ol,ok,h):
    dc_dh = chi(z,om,ol,ok)
    sqrt_ok = sqrt(abs(ok))
    if ok > 0.0:
        return DH/h/sqrt_ok*sinh(sqrt_ok*dc_dh)
    elif ok < 0.0:
        return DH/h/sqrt_ok*sin(sqrt_ok*dc_dh)
    else:
        return DH/h*dc_dh

def get_ok_ol(om,ol):
    if ol is None:
        ol = 1.0 - om
        ok = 0.0
    else:
        ok = 1.0 - ol - om
    return ok,ol
    
def lookback(z,om=OM,ol=None,h=1.0,Na=NZ):
    # do integral in a so it converges OK
    ok,ol = get_ok_ol(om,ol)
    a = 1.0/(1.0 + z)
    da = (1.0 - a)/float(Na)
    return sum(map(lambda a: 1.0/E(1.0/a-1.0,om,ol,ok)/a, \
            (da*i+a for i in xrange(Na))))*da*TH/h

def age(z,om=OM,ol=None,h=1.0):
    t0 = lookback(1e12,om=om,ol=ol,h=h)
    return t0 - lookback(z,om=om,ol=ol,h=h)

def cd(z,om=OM,ol=None,h=1.0):
    ok,ol = get_ok_ol(om,ol)
    return DH/h*chi(z,om,ol,ok)

def ad(z,om=OM,ol=None,h=1.0):
    ok,ol = get_ok_ol(om,ol)
    _dm = dm(z,om,ol,ok,h)
    return _dm/(1.0 + z)

def ld(z,om=OM,ol=None,h=1.0):
    ok,ol = get_ok_ol(om,ol)
    _dm = dm(z,om,ol,ok,h)
    return _dm*(1.0 + z)

