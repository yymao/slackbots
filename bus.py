from datetime import datetime
from bisect import bisect

def minute2str(m):
    m = int(m)
    h = m / 60
    m = m % 60
    p = 'a'
    if h > 12:
        h -= 12
        p = 'p'
    return '{0}:{1:02}{2}'.format(h,m,p)

def find_next_bus(now_m, times):
    i = bisect(times, now_m)
    if i == len(times):
        i = 0
    d = times[i]-now_m
    return d, minute2str(times[i])

from bus_schedule import *

_output_template = '''The next bus from campus@Y2E2 to SLAC departs in {0[0]} minutes (at {0[1]}).
The next bus from SLAC@Kavli to campus departs in {1[0]} minutes (at {1[1]}).
'''

def program(data):
    now = datetime.today()
    if now.weekday() >= 5:
        output = 'There is no SLAC shuttle today.\n'
    else:
        now_m = now.hour * 60 + now.minute + 1
        output = _output_template.format(find_next_bus(now_m, campus_times), \
                find_next_bus(now_m, slac_times))
    output += '(See <http://transportation.stanford.edu/marguerite/slac/|the full schedule here>.)'

    return output
