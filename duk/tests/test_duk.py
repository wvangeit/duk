import sys
import argparse
import types
import pytest
from duk import duk
import unittest.mock as mock

# Import the function to test

def run_parse_arguments_with_args(args):
    """Helper to run parse_arguments with specific sys.argv"""
    old_argv = sys.argv
    sys.argv = ["prog"] + args
    try:
        return duk.parse_arguments()
    finally:
        sys.argv = old_argv

def test_parse_arguments_defaults():
    args = run_parse_arguments_with_args([])
    assert args.dirname == "."
    assert args.nogrouping is False
    assert args.noprogress is False
    assert args.inodes is False
    assert args.noF is False

def test_parse_arguments_with_dirname():
    args = run_parse_arguments_with_args(["/tmp"])
    assert args.dirname == "/tmp"

def test_parse_arguments_nogrouping():
    args = run_parse_arguments_with_args(["--nogrouping"])
    assert args.nogrouping is True

def test_parse_arguments_noprogress():
    args = run_parse_arguments_with_args(["--noprogress"])
    assert args.noprogress is True

def test_parse_arguments_inodes():
    args = run_parse_arguments_with_args(["--inodes"])
    assert args.inodes is True

def test_parse_arguments_noF():
    args = run_parse_arguments_with_args(["--noF"])
    assert args.noF is True

def test_parse_arguments_all_flags_and_dir():
    args = run_parse_arguments_with_args([
        "--nogrouping", "--noprogress", "--inodes", "--noF", "/var"
    ])
    assert args.nogrouping is True
    assert args.noprogress is True
    assert args.inodes is True
    assert args.noF is True
    assert args.dirname == "/var"

def test_parse_arguments_invalid_flag():
    with pytest.raises(SystemExit):
        run_parse_arguments_with_args(["--notaflag"])
def run_parse_arguments_with_args(args):
    """Helper to run parse_arguments with specific sys.argv"""
    old_argv = sys.argv
    sys.argv = ["prog"] + args
    try:
        return duk.parse_arguments()
    finally:
        sys.argv = old_argv

def test_print_error_files_permission_denied(capsys):
    errors = {"file1.txt": "Permission denied", "file2.txt": "Some error"}
    max_marks = 10
    result = duk._print_error_files(errors, max_marks)
    captured = capsys.readouterr()
    assert "Permission denied" in captured.out
    assert "Some error" in captured.out
    assert result is True

def test_print_error_files_no_permission_denied(capsys):
    errors = {"file1.txt": "Some error"}
    max_marks = 10
    result = duk._print_error_files(errors, max_marks)
    captured = capsys.readouterr()
    assert "Some error" in captured.out
    assert result is False

def test_print_normal_files_basic(capsys):
    file_sizes = {"a.txt": 100, "b.txt": 200}
    max_marks = 10
    total_size = 300
    fmt = "{0:<14} {1:<6} {2:<10} {3:<10}"
    class Args:
        nogrouping = False
    duk.print_normal_files(file_sizes, max_marks, total_size, fmt, Args())
    captured = capsys.readouterr()
    assert "a.txt" in captured.out
    assert "b.txt" in captured.out

def test_print_normal_files_nogrouping(capsys):
    file_sizes = {"a.txt": 100}
    max_marks = 5
    total_size = 100
    fmt = "{0:<14} {1:<6} {2:<10} {3:<10}"
    class Args:
        nogrouping = True
    duk.print_normal_files(file_sizes, max_marks, total_size, fmt, Args())
    captured = capsys.readouterr()
    assert "a.txt" in captured.out

def test_calculate_file_sizes_success(tmp_path, monkeypatch):
    # Create files
    f1 = tmp_path / "f1.txt"
    f1.write_text("hello")
    f2 = tmp_path / "f2.txt"
    f2.write_text("world")
    files_list = ["f1.txt", "f2.txt"]
    class Args:
        dirname = str(tmp_path)
        inodes = False
        noF = True
        noprogress = True
    # Patch subprocess.Popen to call real du
    file_sizes, errors = duk.calculate_file_sizes(files_list, Args())
    assert "f1.txt" in file_sizes
    assert "f2.txt" in file_sizes
    assert errors == {}

def test_calculate_file_sizes_permission_denied(monkeypatch):
    files_list = ["badfile"]
    class Args:
        dirname = "/nonexistent"
        inodes = False
        noF = True
        noprogress = True
    def fake_popen(*a, **kw):
        class Proc:
            def communicate(self):
                return (b"", b"Permission denied\n")
        return Proc()
    monkeypatch.setattr(duk.subprocess, "Popen", fake_popen)
    file_sizes, errors = duk.calculate_file_sizes(files_list, Args())
    assert errors
    assert "Permission denied" in list(errors.values())[0]

def test_print_header_inodes(capsys):
    fmt = "{0:<14} {1:<6} {2:<10} {3:<10}"
    class Args:
        inodes = True
    duk.print_header("mydir", fmt, Args())
    captured = capsys.readouterr()
    assert "inodes" in captured.out

def test_print_header_kbyte(capsys):
    fmt = "{0:<14} {1:<6} {2:<10} {3:<10}"
    class Args:
        inodes = False
    duk.print_header("mydir", fmt, Args())
    captured = capsys.readouterr()
    assert "in kByte" in captured.out

def test_print_tail_permission_error(capsys):
    class Args:
        nogrouping = False
    duk.print_tail(12345, True, Args())
    captured = capsys.readouterr()
    assert "Total directory size" in captured.out

def test_print_tail_no_permission_error(capsys):
    class Args:
        nogrouping = True
    duk.print_tail(12345, False, Args())
    captured = capsys.readouterr()
    assert "Total directory size" in captured.out

def test_print_progress(capsys):
    duk.print_progress(0.5, 10)
    captured = capsys.readouterr()
    assert ">" in captured.out or "-" in captured.out
