__all__ = ['sm']
from math import exp, log10

def sm(hm, z=0):
    """stellar mass given halo mass, redshift (Eq. 3 of Behroozi+13)"""
    a = 1.0/(1.0+z)
    loghm = log10(hm)
    logm1 = _logm1(a)
    logsm = _logeps(a) + logm1 + _eff(loghm-logm1, a) - _eff(0., a) 
    return 10.0**logsm

def _eff(x, a):
    alpha, delta, gamma = _alpha(a), _delta(a), _gamma(a)
    f1 = -log10(10.0**(alpha*x)+1.0)
    try:
        f2 = delta*( log10(1.0+exp(x)) )**gamma / (1.+exp(10.0**(-x)))
    except OverflowError:
        f2 = 0.
    return f1 + f2

def _nu(a):
    return exp(-4.0*a*a)

def _logeps(a, eps_0=-1.777, eps_a=-0.006, eps_z=-0.000, eps_a2=-0.119):
    return eps_0 + (eps_a*(a-1.0) + eps_z*(1.0/a-1.0))*_nu(a) + eps_a2*(a-1.0)

def _logm1(a, m1_0=11.514, m1_a=-1.793, m1_z=-0.251):
    return m1_0 + (m1_a*(a-1.0) + m1_z*(1.0/a-1.0))*_nu(a)

def _alpha(a, alpha_0=-1.412, alpha_a=0.731):
    return alpha_0 + (alpha_a*(a-1.0))*_nu(a)

def _delta(a, delta_0=3.508, delta_a=2.608, delta_z=-0.043):
    return delta_0 + (delta_a*(a-1.0) + delta_z*(1.0/a-1.0))*_nu(a)

def _gamma(a, gamma_0=0.316, gamma_a=1.319, gamma_z=0.279):
    return gamma_0 + (gamma_a*(a-1.0) + gamma_z*(1.0/a-1.0))*_nu(a)

def _xi(a, xi_0=0.218, xi_a=-0.023):
    return xi_0 + xi_a*(a-1.0)
