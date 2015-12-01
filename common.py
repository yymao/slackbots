__all__ = ['escape', 'run']
from urllib import urlopen

_error_template = '*Something went wrong and this result couldn\'t be posted directly onto the channel.*\n{0}\nDebugging info: {1}\npayload = {2}'

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', r'\"')

def run(program, data, token=None, incoming_url=None):
    if token and data['token'] != token:
        return 
    output = program(data)
    if incoming_url and isinstance(output, tuple):
        output, payload = output
        try:
            res = urlopen(incoming_url, data=payload).read().strip()
        except IOError:
            res = 'IOError'
        if res == 'ok':
            output = ''
        else:
            output = _error_template.format(output, escape(res), payload)
    return output

