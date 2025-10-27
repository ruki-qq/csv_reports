import logging
from contextlib import redirect_stdout
from io import StringIO

from main import main


def test_main_success(temp_csv_file, caplog):
    caplog.set_level(logging.DEBUG)
    captured_stdout = StringIO()
    exit_code = 0
    with redirect_stdout(captured_stdout):
        try:
            main(["--files", str(temp_csv_file), "--report", "average-rating"])
        except SystemExit as e:
            exit_code = e.code

    stdout = captured_stdout.getvalue()
    assert exit_code == 0
    assert "average-rating" in stdout and "╭" in stdout
    assert "apple" in stdout and "samsung" in stdout
    assert "Successfully created table" in caplog.text


def test_main_missing_file(nonexistent_file, caplog):
    caplog.set_level(logging.DEBUG)
    exit_code = 0
    try:
        main(["--files", str(nonexistent_file), "--report", "average-rating"])
    except SystemExit as e:
        exit_code = e.code

    assert exit_code == 1
    assert (
        "File nonexistent_file.csv does not exist!" in caplog.text
        and "No products found." in caplog.text
    )


def test_main_empty_file(empty_csv_file, caplog):
    caplog.set_level(logging.DEBUG)
    exit_code = 0
    try:
        main(["--files", str(empty_csv_file), "--report", "average-rating"])
    except SystemExit as e:
        exit_code = e.code

    assert exit_code == 1
    assert "is empty!" in caplog.text and "No products found" in caplog.text


def test_main_unknown_report(temp_csv_file, caplog):
    caplog.set_level(logging.DEBUG)
    exit_code = 0
    try:
        main(["--files", str(temp_csv_file), "--report", "non-average-rating"])
    except SystemExit as e:
        exit_code = e.code

    assert exit_code == 1
    assert "Report 'non-average-rating' isn't found." in caplog.text
