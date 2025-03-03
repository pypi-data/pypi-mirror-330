import pytest, os
from datetime import datetime, timedelta
from unittest.mock import patch
from task_6.src.f1_report_by_viacent.cli import main
from task_6.src.f1_report_by_viacent.functions import (
    process_file, process_abbrev_line, process_log_line,parse_logs,
    calculate_lap_times, build_report, format_time, print_report,
    driver_report)


@pytest.fixture
def mock_log_files(tmp_path):
    """
    Creates temporary files with test race log data.
    """
    abbreviations_content = """VET_Sebastian Vettel_Ferrari
HAM_Lewis Hamilton_Mercedes"""
    start_log_content = """VET2018-05-24_12:02:02.222
HAM2018-05-24_12:03:03.333"""
    end_log_content = """VET2018-05-24_12:04:04.444
HAM2018-05-24_12:06:06.666"""
    abbreviations_file = tmp_path / "abbreviations.txt"
    start_file = tmp_path / "start.log"
    end_file = tmp_path / "end.log"
    abbreviations_file.write_text(abbreviations_content)
    start_file.write_text(start_log_content)
    end_file.write_text(end_log_content)
    return str(tmp_path)

def test_process_abbrev_line():
    """
    Test for processing a string from abbreviations.txt
    """
    assert process_abbrev_line("VET_Sebastian Vettel_Ferrari") == ("VET", ["Sebastian Vettel", "Ferrari"])

def test_log_line_start():
    """
    Test of processing a line from start.log
    """
    result = process_log_line("VET2018-05-24_12:02:02.222")
    assert result[0] == "VET"
    assert isinstance(result[1], datetime)

def test_log_line_end():
    """
    Test of processing a line from end.log
    """
    result = process_log_line("HAM2018-05-24_12:06:06.666")
    assert result[0] == "HAM"
    assert isinstance(result[1], datetime)

def test_process_abbrev_line_invalid():
    """
    Error test if string format is incorrect
    """
    with pytest.raises(ValueError,  match="Invalid line format in abbreviation.txt: INVALID_FORMAT"):
        process_abbrev_line("INVALID_FORMAT")

def test_process_log_line_invalid_short():
    """
    Test processing a log line that is too short.
    """
    with pytest.raises(ValueError, match=r"Invalid log line format: AB"):
        process_log_line("AB")

def test_process_log_line_valid():
    """
    Test processing a valid log line.
    """
    abbreviation, time = process_log_line("VET2018-05-24_12:02:02.222")
    assert abbreviation == "VET"
    assert isinstance(time, datetime)
    assert time == datetime(2018, 5, 24, 12, 2, 2, 222000)

def test_process_file(mock_log_files):
    """
    File reading test
    """
    file_path = os.path.join(mock_log_files, "abbreviations.txt")
    data = process_file(file_path, process_abbrev_line)
    assert data["VET"] == ["Sebastian Vettel", "Ferrari"]
    assert data["HAM"] == ["Lewis Hamilton", "Mercedes"]

def test_process_file_not_found():
    """
    Error test if file not found
    """
    with pytest.raises(FileNotFoundError, match="File not found: nonexistent.txt"):
        process_file("nonexistent.txt", lambda line: line)

def test_process_file_permission_error(mocker, tmp_path):
    """
    Permission error test when opening a file
    """
    file_path = tmp_path / "test.txt"
    file_path.write_text("Test content")  # Создаём реальный файл
    mocker.patch("builtins.open", side_effect=PermissionError("Permission denied"))
    with pytest.raises(RuntimeError, match="Unable to open or read file: .* Permission denied"):
        process_file(str(file_path), lambda line: line)

def test_parse_logs(mock_log_files):
    """
    Log parsing test
    """
    data = parse_logs(mock_log_files)
    assert "VET" in data["abbreviations"]
    assert data["abbreviations"]["VET"] == ["Sebastian Vettel", "Ferrari"]
    assert "VET" in data["start_times"]
    assert isinstance(data["start_times"]["VET"], datetime)
    assert "VET" in data["end_times"]
    assert isinstance(data["end_times"]["VET"], datetime)

def test_calculate_lap_times(mock_log_files):
    """
    Lap time calculation test
    """
    data = parse_logs(mock_log_files)
    lap_times = calculate_lap_times(data)
    assert len(lap_times) == 2
    assert lap_times[0]["abbreviation"] == "VET"
    assert lap_times[0]["lap_time"] == timedelta(minutes=2, seconds=2, microseconds=222000)

def test_build_report(mock_log_files):
    """
    Report generation test
    """
    report = build_report(mock_log_files, order="asc")
    assert report[0]["abbreviation"] == "VET"
    assert report[1]["abbreviation"] == "HAM"
    report_desc = build_report(mock_log_files, order="desc")
    assert report_desc[0]["abbreviation"] == "HAM"
    assert report_desc[1]["abbreviation"] == "VET"

def test_format_time():
    """
    Lap time formatting test
    """
    assert format_time(timedelta(minutes=1, seconds=30, microseconds=500000)) == "1:30.500"
    assert format_time(timedelta(minutes=3, seconds=23)) == "3:23.000"
    assert format_time(timedelta(minutes=5)) == "5:00.000"

def test_print_report(mock_log_files, capsys):
    """
    Report output test
    """
    report = build_report(mock_log_files)
    print_report(report * 10)
    captured = capsys.readouterr()
    assert "Top 15 Racers" in captured.out
    assert "Sebastian Vettel" in captured.out
    assert "Lewis Hamilton" in captured.out
    assert "Rest of the Racers:" in captured.out
    assert ("-" * 80) in captured.out

def test_driver_report(mock_log_files, capsys):
    """
    Test displaying information about a specific racer.
    """
    report = build_report(mock_log_files)
    driver_report(report, "Sebastian Vettel")
    captured = capsys.readouterr()
    assert "Driver: Sebastian Vettel" in captured.out
    assert "Team: Ferrari" in captured.out
    assert "Lap Time: 2:02.222" in captured.out

def test_missing_files_arg(capfd):
    """
    Error test if --files argument is not passed.
    """
    with patch("sys.argv", ["cli.py", "--asc"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    captured = capfd.readouterr()
    assert "the following arguments are required: --files" in captured.err
    assert excinfo.value.code != 0

def test_invalid_order_arg(mock_log_files, capfd):
    """
    Error test if both --asc and --desc are passed at the same time.
    """
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--asc", "--desc"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    captured = capfd.readouterr()
    assert "Dont use both --asc & --desc" in captured.err
    assert excinfo.value.code != 0

def test_valid_asc_order(mock_log_files, capfd):
    """
    Test the correct operation of the command with ascending sort asc.
    """
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--asc"]):
        main()
    captured = capfd.readouterr()
    assert "Top 15 Racers:" in captured.out
    assert captured.err == ""

def test_valid_desc_order(mock_log_files, capfd):
    """
    Test the correct operation of the command with sorting in descending order desc.
    """
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--desc"]):
        main()
    captured = capfd.readouterr()
    assert "Top 15 Racers:" in captured.out
    assert captured.err == ""

def test_valid_driver_report(mock_log_files, capfd):
    """
    Test the correct request for information about a specific racer.
    """
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--driver", "Sebastian Vettel"]):
        main()
    captured = capfd.readouterr()
    assert "Driver: Sebastian Vettel" in captured.out
    assert "Team: Ferrari" in captured.out
    assert captured.err == ""

def test_invalid_driver_report(mock_log_files, capfd):
    """
    Test error output if a non-existent racer is requested.
    """
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--driver", "unknown driver"]):
        main()
    captured = capfd.readouterr()
    assert "No data found for driver" in captured.out
    assert captured.err == ""
