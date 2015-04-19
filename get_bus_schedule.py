from urllib import urlopen
from bs4 import BeautifulSoup

def str2minute(s):
    t, __, p = s.partition(' ')
    h, __, m = t.partition(':')
    h = int(h)
    if p == 'p' and h < 12:
        h += 12
    return h*60 + int(m)

if __name__ == '__main__':
    url = 'http://transportation.stanford.edu/marguerite/slac/'
    soup = BeautifulSoup(urlopen(url).read())
    times = [t.text.encode('utf-8') for t in soup.findAll('td')]

    campus = 1
    slac = 8
    total = 16

    campus_times = map(str2minute, \
            filter(lambda s: s != '-', times[campus::total]))
    slac_times = map(str2minute, \
        filter(lambda s: s != '-', times[slac::total]))

    with open('bus_schedule.py', 'w') as f:
        f.write('slac_times=[{0}]\n'.format(','.join(map(str, slac_times))))
        f.write('campus_times=[{0}]\n'.format(','.join(map(str, campus_times))))

