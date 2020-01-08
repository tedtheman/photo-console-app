"""
pytest cases for photos.py

@author: Ted Nienstedt
"""

import builtins
import re
import photos

INPUT_RESPONSE = []  # for monkeypatching with send_input() and patch_input()


def arg_list(arg_str):
    """arg list builder from given string"""
    return list(arg_str.split(' '))


def compare(a, b):
    """ Compare two base strings, disregarding whitespace """
    return re.sub(r"\s*", "", a) == re.sub(r"\s*", "", b)


def verify(capsys, test_case):
    """"Verify stdout contains expected output"""
    std_out, _ = capsys.readouterr()  # ignore stderr

    out_path = f"out/{test_case}.out"
    with open(out_path, mode='w') as file_out:
        print(std_out, file=file_out, end='')  # drop newline

    in_path = f"ctl/{test_case}.out"
    with open(in_path, mode='r') as file_in:
        ctl = file_in.read()

    assert compare(std_out, ctl) is True


def send_input(value, **kwargs):  # pylint: disable=unused-argument
    """"Simulate user input with given string or a stack of strings"""
    global INPUT_RESPONSE  # pylint: disable=global-statement
    print(value, end='')
    if isinstance(INPUT_RESPONSE, list):
        if len(INPUT_RESPONSE):
            retval = INPUT_RESPONSE[0]
        else:
            retval = ''
        INPUT_RESPONSE = INPUT_RESPONSE[1:]  # pop stack
        if len(INPUT_RESPONSE) >= 1:
            print()
    else:
        retval = INPUT_RESPONSE
    return retval


def set_input(response):
    """"Mock set input value"""
    global INPUT_RESPONSE  # pylint: disable=global-statement
    INPUT_RESPONSE = response


def patch_input(monkeypatch, response=None):
    """"Mock input method"""
    global INPUT_RESPONSE  # pylint: disable=global-statement
    monkeypatch.setattr(builtins, 'input', send_input)
    if response:
        INPUT_RESPONSE = response


def patch_url(monkeypatch, suffix):
    """Override URL constant to force bad URL error"""
    orig_url = getattr(photos, 'PHOTOS_URL')
    monkeypatch.setattr(photos, 'PHOTOS_URL', orig_url + suffix)


def test_help(capsys):
    """Capture and verify expected help info"""
    # --help does SystemExit so we need to catch it
    try:
        photos.main(arg_list('-h'))
    except SystemExit:
        pass
    verify(capsys, 'help')


def test_def_interactive_prompts(capsys, monkeypatch):
    """unit test the interactive_prompts function"""
    def mock_get_album_info(album_id):
        return None
    monkeypatch.setattr(photos, 'get_album_info', mock_get_album_info)

    patch_input(monkeypatch)
    for resp in [['1', '-1', 'a', '1'], 'q', '0', ['', '']]:
        set_input(resp)
        photos.interactive_prompts()

    verify(capsys, 'def_interactive_prompts')


def test_no_args(capsys, monkeypatch):
    """Verify no argument behavior"""
    patch_input(monkeypatch, response='q')
    photos.main([])
    verify(capsys, 'no_args')


def test_interactive(capsys, monkeypatch):
    """Verify series of interactive album ids"""
    patch_input(monkeypatch, response=['2', '3', '0'])
    photos.main([])
    verify(capsys, 'interactive_test')


def test_exit_with_two_empty_returns(capsys, monkeypatch):
    """Verify exit via two empty returns"""
    patch_input(monkeypatch, response=['', ''])
    photos.main([])
    verify(capsys, 'exit_with_two_empty_returns')


def test_0(capsys):
    """Verify expected response from album id of zero"""
    photos.main(arg_list('0'))
    verify(capsys, 'album_0')


def test_1(capsys):
    """Verify Album 1"""
    photos.main(arg_list('1'))
    verify(capsys, 'album_1')


def test_2_max5(capsys):
    """Verify first 5 rows of Album 2 in prettyTable format"""
    photos.main(arg_list('2 -n 5 --pretty'))
    verify(capsys, 'album_2_max5_pretty')


def test_3_max5(capsys):
    """Verify first 5 rows of Album 3 with relative row numbers ouput"""
    photos.main(arg_list('3 -n 5 --rows'))
    verify(capsys, 'album_3_max5_rows')


def test_3_grep_qui(capsys):
    """Verify row filtering with expected matches"""
    photos.main(arg_list('3 --grep qui --rows --pretty'))
    verify(capsys, 'album_3_grep_qui')


def test_3_grep_nomatch(capsys):
    """Verify row filtering with no matches"""
    photos.main(arg_list('3 --grep NOMATCH --rows --pretty'))
    verify(capsys, 'album_3_grep_nomatch')


def test_3_bad_grep(capsys):
    """Verify handling of invalid grep pattern"""
    photos.main(arg_list('3 --grep "][" --rows --pretty'))
    verify(capsys, 'album_3_bad_grep')


def test_35_100_max20(capsys):
    """Verify multiple Album ids with max row number for each"""
    photos.main(arg_list('35 100 -n 20'))
    verify(capsys, 'album_35+100_max20')


def test_101(capsys):
    """Verify non-existing Album number with debug enabled"""
    photos.main(arg_list('101 -d'))
    verify(capsys, 'album_101')


def test_bad_albumid(capsys):
    """Verify handling of invalid Album id"""
    photos.main(arg_list('x'))
    verify(capsys, 'bad_album_id')


def test_bad_albumid_interactive(capsys, monkeypatch):
    """Verify handling of invalid Album id in interactive mode"""
    patch_input(monkeypatch, response=['1', 'bad', '0'])
    photos.main([])
    verify(capsys, 'bad_album_id_interactive')


def test_timeout(capsys):
    """Verify handling of timeout accessing URL"""
    photos.main(arg_list('99 -t .01'))
    verify(capsys, 'timeout_test')


def test_bad_url(capsys, monkeypatch):
    """Verify handling of bad or unrecognized URL"""
    patch_url(monkeypatch, 'x')
    photos.main(['1'])
    verify(capsys, 'bad_url')
