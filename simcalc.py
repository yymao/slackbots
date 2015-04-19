_rho_c = 2.7745945707e+11

_help_msg = '''*Syntax*: /simcalc [boxsize] [Np] [mass] [[OmegaM]]
Put one ? in the field that you want to find out. 

[boxsize] is in Mpc/h, [mass] is in Msun/h, [OmegaM] is optional and default to 0.3.
Also, [Np] and [boxsize] are the number on the side.'''

def program(data):
    query = data['text'].split()

    if len(query) < 2:
        return _help_msg
    if len(query) == 2:
        query.append('?')
    if len(query) == 3:
        query.append((0.3 if '?' in query else '?'))
    
    try:
        i = query.index('?')
    except IndexError:
        return _help_msg

    query[i] = 0
    try:
        box_size, N, m, Omega_M = map(float, query)
    except (ValueError, TypeError):
        return _help_msg

    if i == 0:
        output = 'if Np = {0:g}, mass = {1:g} Msun/h, and OmegaM = {2:g} \nthen boxsize = {3:g} Mpc/h'.format(\
                N, m, Omega_M, N*(m/_rho_c/Omega_M)**(1.0/3.0))

    elif i == 1:
        output = 'if boxsize = {0:g} Mpc/h, mass = {1:g} Msun/h, and OmegaM = {2:g} \nthen Np = {3}'.format(\
                box_size, m, Omega_M, int(box_size*(_rho_c*Omega_M/m)**(1.0/3)))

    elif i == 2:
        output = 'if boxsize = {0:g} Mpc/h, Np = {1:g}, and OmegaM = {2:g} \nthen particle mass = {3:g} Msun/h'.format(\
                box_size, N, Omega_M, (box_size/N)**3*_rho_c*Omega_M)

    elif i == 3:
        output = 'if boxsize = {0:g} Mpc/h, Np = {1:g}, and mass = {2:g} Msun/h \nthen OmegaM = {3:g}'.format(\
                box_size, N, m, (N/box_size)**3*m/_rho_c)

    return output

