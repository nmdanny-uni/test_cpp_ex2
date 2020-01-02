from __future__ import annotations
import os
from dataclasses import dataclass
import sys
from pathlib import Path
import pytest
import subprocess
from typing import List
from tempfile import NamedTemporaryFile

USE_VALGRIND = True

TEST_DIR = Path(__file__).parent

EXECUTABLE_PATH = Path(Path(TEST_DIR) / "../cmake-build-debug/FractalDrawer")
SCHOOL_EXECUTABLE = Path(Path(TEST_DIR) / "./SchoolFractalDrawer")

if not EXECUTABLE_PATH.exists():
    print(f"Couldn't find your executable at {EXECUTABLE_PATH}", file=sys.stderr)
    sys.exit(-1)

if not SCHOOL_EXECUTABLE.exists():
    print(f"Couldn't find school executable at {SCHOOL_EXECUTABLE}", file=sys.stderr)
    sys.exit(-1)

VALID_DIR = TEST_DIR / "valid"
INVALID_DIR = TEST_DIR / "invalid"

VALID_CSVS = [ str(VALID_DIR / path) for path in os.listdir(VALID_DIR)]
INVALID_CSV = [ str(INVALID_DIR / path) for path in os.listdir(INVALID_DIR)]

@dataclass
class Output:
    return_code: int
    stdout: str
    stderr: str
    valgrind_out: str

    def compare_to(self, other: Output):
        # "self" is the school's output and "other" is YOUR output
        assert self.return_code == other.return_code, "Return code mismatch(left=school, right=yours)"
        assert self.stdout == other.stdout, "STDOUT mismatch(left=school, right=yours)"
        assert self.stderr == other.stderr, "STDERR mismatch(left=school, right=yours)"

    def check_valgrind_out(self):
        if "ERROR SUMMARY: 0" not in self.valgrind_out:
            print(f"Valgrind failed:\n{self.valgrind_out}", file=sys.stderr)

def run_with_cmd(command_list: List[str], str="", valgrind=False) -> Output:
    """
    Execute the given command list with the input
    """
    valgrind_outfile, valgrind_output = None, ""
    if valgrind:
        valgrind_outfile = NamedTemporaryFile(mode='r+', encoding='utf-8')
        command_list = ['valgrind', '--leak-check=yes', f'--log-file={valgrind_outfile.name}'] + command_list

    print(f"Running command \"{' '.join(command_list)}\"")
    try:
        process = subprocess.run(command_list, shell=False, input=str,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)

        if valgrind:
            valgrind_outfile.seek(0)
            valgrind_output = valgrind_outfile.read()
            valgrind_outfile.close()

        return Output(process.returncode, process.stdout, process.stderr, valgrind_output)
    except Exception as e:
        print(f"Error while running subprocess: {e}")
        sys.exit(-1)


def _test_csv(csv_path: str):
    my_out = run_with_cmd([str(EXECUTABLE_PATH), csv_path], valgrind=USE_VALGRIND)
    school_out = run_with_cmd([str(SCHOOL_EXECUTABLE), csv_path], valgrind=False)
    school_out.compare_to(my_out)
    if USE_VALGRIND:
        my_out.check_valgrind_out()


@pytest.mark.parametrize("path", VALID_CSVS)
def test_valid(path: str):
    _test_csv(path)


@pytest.mark.parametrize("path", INVALID_CSV)
def test_invalid(path: str):
    if Path(path).suffix != ".csv":
        # the school's solution doesn't check for valid extension, so I test this differently
        my_out = run_with_cmd([str(EXECUTABLE_PATH), path], valgrind=USE_VALGRIND)
        assert "Invalid input\n" == my_out.stderr, "A non .csv file should result in 'Invalid Input' error message"
        assert 0 != my_out.return_code, "A non .csv file should result in a non-zero return code"
        assert "" == my_out.stdout, "Upon failure, nothing should be emitted to STDOUT"
        return
    _test_csv(path)


if __name__ == '__main__':
    exit_code = pytest.main([__file__, '-vvs'])
    sys.exit(exit_code)
