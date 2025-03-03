# tests/test_easyprint.py

from easyprintstr import print_with_border

def test_print_with_border(capsys):
    print_with_border("Test")
    captured = capsys.readouterr()
    assert captured.out == "*******\n* Test *\n*******\n"