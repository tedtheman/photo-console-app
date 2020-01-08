"""
Photo Album console application.

The purpose is to display photo ids and tiles in an album.

Photo information is stored in a JSON file at the following URL:
    https://jsonplaceholder.typicode.com/photos

To select a given album id, <n>, append it to the UTL as follows:
    ?albumId=<n>.

Example for the album id of 3:
    https://jsonplaceholder.typicode.com/photos?albumId=3

    @author: Ted Nienstedt

"""

import sys
import argparse
import re
import requests
from prettytable import PrettyTable

PHOTOS_URL = 'https://jsonplaceholder.typicode.com/photos'
FIELD_NAMES = ["PhotoId", "Title"]


class RunOpts:  # pylint: disable=too-few-public-methods
    """RunOpts object."""

    opts = None
    debug = False
    title_pattern = None

    def __init__(self):
        self.opts = RunOpts.opts
        self.debug = RunOpts.debug
        self.title_pattern = RunOpts.title_pattern


RUN_OPTS = RunOpts()


def main(given_args):
    """Photo app main method."""
    opts = parse_args(given_args)
    RUN_OPTS.opts = opts

    if 'debug' in opts:
        RUN_OPTS.debug = opts['debug']
        print_debug('debug enabled')

    # force interactive mode if no album(s) given
    if len(opts['albums']) == 0 and not opts['interactive']:
        print_debug("forcing interactive mode on")
        opts['interactive'] = True

    if opts['grep']:
        try:
            RUN_OPTS.title_pattern = re.compile(opts['grep'])
        except Exception as error:  # pylint: disable=broad-except
            print(f"ignoring invalid regex \"{opts['grep']}\": {error}")

    nbr_albums = len(opts['albums'])

    print_debug(f"{nbr_albums} album(s) given")

    for album_id in opts['albums']:
        if not album_id.isdigit():
            print("albumId must be numeric")
            continue
        if nbr_albums > 1:
            print(f"### album id {album_id} ###")

        photos = get_album_info(album_id)

        if photos:
            display_album_info(photos)

    if opts['interactive']:
        interactive_prompts()


def interactive_prompts():
    """Interactive prompter."""
    prev_album_id = None
    while True:
        album_id = input("Enter album_id: ").strip()
        if album_id == '':
            if prev_album_id == '':
                print('two empty responses, exiting ...')
                break
            prev_album_id = album_id
            continue
        if album_id in ('0', 'q'):
            print('exiting ...')
            break
        if not album_id.isdigit():
            print("invalid albumId, should be 1-100, see -h/--help")
            prev_album_id = album_id
            continue

        photos = get_album_info(album_id)

        if photos:
            display_album_info(photos)


def get_album_info(album_id):
    """get album info"""
    opts = RUN_OPTS.opts

    payload = {'albumId': album_id}
    try:
        resp = requests.get(PHOTOS_URL, params=payload,
                            timeout=opts['timeout'])
    except (requests.ConnectionError, requests.ReadTimeout):
        print(f"get for {PHOTOS_URL} errored or timed out after " +
              f"{opts['timeout']} seconds")
        return None

    print_debug(f"http status_code = {resp.status_code}; url = {resp.url}")

    if not resp.ok:
        print(f'url for album_id={album_id} or "{resp.url}" not found: ' +
              f'status {resp.status_code}')
        return None

    photos = resp.json()
    if not resp.ok or len(photos) <= 0:
        print(f'zero rows returned for album_id={album_id}')
        return None

    return photos


def display_album_info(photos):  # pylint: disable=too-many-branches
    """Display album information."""
    opts = RUN_OPTS.opts

    if opts['rows']:
        field_names = ["Row"] + FIELD_NAMES
    else:
        field_names = FIELD_NAMES

    if opts['pretty']:
        ptable = PrettyTable(field_names=field_names)
        ptable.align['Title'] = 'l'  # left justify titles
    else:
        ptable = None

    for row, album in enumerate(photos, 1):

        if RUN_OPTS.title_pattern:
            result = RUN_OPTS.title_pattern.search(album['title'])
            if not result:
                continue

        display_album_row(ptable, row, album['id'], album['title'])

        if opts['number'] and opts['number'] <= row:
            break

    if opts['pretty']:
        print(ptable)


def display_album_row(ptable, row, id, title):
    """display album row"""
    opts = RUN_OPTS.opts

    if opts['pretty'] and ptable:
        if opts['rows']:
            ptable.add_row([row, id, title])
        else:
            ptable.add_row([id, title])
    else:
        if opts['rows'] and row != int(id):
            print(f"[{id}:{row}] {title}")
        else:
            print(f"[{id}] {title}")


def print_debug(debug_str):
    """Debug print handler."""
    if RUN_OPTS.debug:
        print(f"Debug: {debug_str}")


def parse_args(args):
    """Argment parsing handler."""
    # note: use RawDescriptionHelpFormatter to allow newlines
    parser = argparse.ArgumentParser(
        prog='photos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Display photo ids and titles for given album id(s).
Provide album ids via command line and/or interactive prompts.
Valid album ids are 1-100.
To exit interactive mode enter 0, 'q' or hit return twice in succession.
""",
        epilog="""Examples:
photos 3 -i      # begin with album 3 and prompt for more
photos 1 99 -r   # print albums 1 and 99 with row numbers
photos -p -r 3   # output prettyprint table with row numbers.
""")

    parser.add_argument('-d', '--debug', action='store_true',
                        help='print debug info.')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='prompt for album id(s).')
    parser.add_argument('-g', '--grep', action='store', type=str, default='',
                        help='regex pattern for matching titles')
    parser.add_argument('-n', '--number', action='store', type=int, default=0,
                        help='max number of photos to show (default all).')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='use PrettyTable for showing album info.')
    parser.add_argument('-r', '--rows', action='store_true',
                        help='include row counts in output.')
    parser.add_argument('-t', '--timeout', action='store', type=float,
                        default=5,
                        help='timeout in seconds for photo album url.')
    parser.add_argument('albums', nargs='*', default='',
                        help='optional album id(s) ...')

    args_namespace = parser.parse_args(args)

    return vars(args_namespace)  # return dict of parsed args namespace


if __name__ == '__main__':

    main(sys.argv[1:])      # pragma: no cover
