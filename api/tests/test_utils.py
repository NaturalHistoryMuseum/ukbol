from ukbol.utils import log


def test_log(capsys):
    message = "testing this thing"
    log(message)
    logged_text = capsys.readouterr().out
    assert logged_text.endswith(f"{message}\n")
