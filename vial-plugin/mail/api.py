import os.path

from email.parser import HeaderParser
from email.utils import getaddresses
from email.header import decode_header

from unidecode import unidecode


def get_book(fname):
    result = []
    for line in open(fname):
        addr, title = line.rstrip('\r\n').split('\t')
        try:
            title = title.decode('utf-8')
        except UnicodeDecodeError:
            title = title.decode('cp1251')

        result.append(('{} {}'.format(addr, unidecode(title)).lower(),
                       '{} <{}>'.format(title.encode('utf-8'), addr) if title else addr))

    return sorted(result)


def dheader(header):
    parts = decode_header(header)
    result = u''
    for r, enc in parts:
        enc = enc or 'ascii'
        result += r.decode(enc)

    return result.encode('utf-8')


def get_addresses(maildir):
    emails = {}
    for root, _dirs, files in os.walk(maildir):
        for fname in files:
            fname = os.path.join(root, fname)
            msg = HeaderParser().parse(open(fname))

            froms = msg.get_all('from', [])
            tos = msg.get_all('to', [])
            ccs = msg.get_all('cc', [])
            resent_tos = msg.get_all('resent-to', [])
            resent_ccs = msg.get_all('resent-cc', [])
            all_recipients = getaddresses(froms + tos + ccs + resent_tos + resent_ccs)
            for (title, addr) in all_recipients:
                emails.setdefault(addr, set()).add(title)

    for addr, titles in emails.iteritems():
        clean = set()
        for title in titles:
            if title.startswith('=?'):
                title = dheader(title)

            title = title.strip("'\"<>").replace('\n', ' ')
            if title and title != addr:
                clean.add(title)

        if clean:
            for title in clean:
                yield addr, title
        else:
            yield addr, ''
