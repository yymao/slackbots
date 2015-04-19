from datetime import datetime
from bisect import bisect
from bus_schedule import *

def minute2str(m):
    m = int(m)
    h = m / 60
    m = m % 60
    p = 'a'
    if h > 12:
        h -= 12
        p = 'p'
    return '{0}:{1:02}{2}'.format(h,m,p)

def find_next_bus(now_m, times, direction_text):
    i = bisect(times, now_m)
    if i == len(times):
        return False, 'There\'s no more buses {0} today.\n'.format(direction_text)
    d = times[i]-now_m
    return True, 'The next bus {0} departs in {1} minute{2} (at {3}).\n'.format(\
            direction_text, d, 's' if d > 1 else '', minute2str(times[i]))

def program(data):
    now = datetime.today()
    if now.weekday() >= 5:
        output = 'Oops... There\'s no SLAC buses running today.\n'
    else:
        now_m = now.hour * 60 + now.minute + 1
        has_bus1, output1 = find_next_bus(now_m, campus_times, \
                'from campus@Y2E2 to SLAC')
        has_bus2, output2 = find_next_bus(now_m, slac_times, \
                'from SLAC@Kavli to campus')
        if has_bus1 or has_bus2:
            output = output1 + output2
        else:
            output = 'Oops... There\'s no more SLAC buses running today.\n'
    output += '(See the <http://transportation.stanford.edu/marguerite/slac/|full schedule here>.)'

    return output
