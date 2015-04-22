import re
from urllib import quote_plus
import math
from common import escape

_globals = {'__builtins__':{}}

_locals = vars(math)
try:
    import cosmo
except ImportError:
    pass
else:
    for k in cosmo.__all__:
        _locals[k] = cosmo.__dict__[k]

_help_msg = '''Supports most simple math functions and the following cosmology functions:
- `cd`: comoving distance [Mpc]
- `ld`: luminosity distance [Mpc]
- `ad`: angular distance [Mpc]
- `age`: age of the universe [Gyr]
- `lookback`: lookback time [Gyr]
All cosmology functions have this call signature: `(z, om=0.3, ol=1-om, h=1)`. Note that h is default to 1.'''

_escape_pattern = r'[^A-Za-z0-9\-+*/%&|~!=()<>.,#]|\.(?=[A-Za-z_])'

_error_msg = '''Hmmm... something\'s wrong with the input expression.
Type `/calc help` to see supported cosmology functions.
Or just try asking <https://www.google.com/?#q={0}|Google>.'''

def program(data):
    expr = data['text'].strip()
    if expr in ['', '-h', '--help', 'help']:
        return _help_msg

    escaped_expr = re.sub(_escape_pattern, '', expr.replace('^', '**'))

    try:
        ans = eval(escaped_expr, _globals, _locals)
    except:
        ans = _error_msg.format(escape(quote_plus(expr,'')))
    else:
        if isinstance(ans, float):
            ans = '= {0:g}'.format(ans)
        else:
            ans = '= {0}'.format(ans)

    return '{0}\n{1}'.format(escape(expr), ans)

