import os.path
from unidecode import unidecode

from vial import vim
from vial.utils import single
from .api import get_book, get_addresses

MAILDIR = os.path.expanduser('~/mail')
BOOK = os.path.expanduser('~/mail/addresses')
cached_book = single(get_book, BOOK)


def update():
    with open(BOOK, 'w') as f:
        for addr, title in get_addresses(MAILDIR):
            f.write('{}\t{}\n'.format(addr, title))


def omnifunc(findstart, base):
    if findstart in (0, b'0'):
        q = unidecode(base.decode('utf-8')).lower()
        book = cached_book()
        return [r[1] for r in book if q in r[0]]
    else:
        vim.command('norm! b')
        return vim.current.window.cursor[1]
