import re
from fetch_arxiv import fetch_arxiv, arxiv_re
from common import escape

_error_msg = '''*Syntax*: /arxiv [arxiv id] [[comments]]
Please provide a valid arxiv ID.'''

_output_template = u'{3}> [<http://arxiv.org/abs/{0}|{0}>] (<http://arxiv.org/pdf/{0}.pdf|PDF>) *{1}* by {2}'

_payload_template = '{{"channel": "{0}", "username": "{1} via arxivbot", "text": "{2}", "link_names": 1}}'


def _format_authors(authors, n=6):
    return ', '.join(authors[:n]) + (' et al.' if len(authors) > n else '')


def program(data):
    query, __, comment = data['text'].strip().partition(' ')
    if comment:
        comment = escape(comment) + r'\n'

    arxiv_id = arxiv_re.search(query)
    if arxiv_id is None:
        return _error_msg
    arxiv_id = arxiv_id.group()

    entry = fetch_arxiv(id_list=arxiv_id).iterentries().next()
    if entry is None or entry.entry is None:
        return _error_msg

    output = _output_template.format(entry['key'], \
            escape(re.sub(r'\s+', u' ', entry['title'], re.U)), \
            escape(_format_authors(entry['authors'])), \
            comment).encode('utf-8')

    payload = _payload_template.format(data['channel_id'], data['user_name'], \
            output)

    return output, payload

