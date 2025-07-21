import os
import sys
from pathlib import Path
from subprocess import check_output, run
from typing import TextIO

import pytest

sources = (
    ("A", "dsu_practice.py"),
    ("B", "fenwick_practice.py"),
    ("C", "floor_sum_practice.py"),
    ("D", "maxflow_practice.py"),
    ("E", "mincostflow_practice.py"),
    ("F", "convolution_practice.py"),
    ("F", "convolution_practice_int.py"),
    ("G", "scc_practice.py"),
    ("H", "twosat_practice.py"),
    ("I", "sa_practice.py"),
    ("J", "segtree_practice.py"),
    ("J", "segtree_practice_reversed.py"),
    ("K", "lazysegtree_practice_k.py"),
    ("K", "lazysegtree_practice_k_wo_modint.py"),
    ("L", "lazysegtree_practice_l.py"),
)


def run_example(source: str, stdin: TextIO) -> str:
    source_path = Path(__file__).parent.parent.parent / "example" / source
    output = check_output((sys.executable, source_path), stdin=stdin)
    return output.decode().replace(os.linesep, "\n")


def combine(source: str, output: str) -> None:
    source_path = Path(__file__).parent.parent.parent / "example" / source
    run((sys.executable, "-m", "atcoder", source_path, "-o", output))


class TestExamples:
    @pytest.mark.parametrize("problem_id, source", sources)
    def test_examples(self, problem_id: str, source: str) -> None:
        input_path = Path(__file__).parent / "input"
        stdin_paths = list(input_path.glob(f"{problem_id}*_in.txt"))
        stdout_paths = list(input_path.glob(f"{problem_id}*_out.txt"))
        stdin_paths.sort()
        stdout_paths.sort()

        for stdin_path, stdout_path in zip(stdin_paths, stdout_paths, strict=False):
            with open(stdin_path) as stdin:
                output = run_example(source, stdin)

            with open(stdout_path) as stdout:
                assert output == stdout.read()

    @pytest.mark.parametrize("problem_id, source", sources)
    def test_combined_examples(self, problem_id: str, source: str) -> None:
        tmp_dir = Path(__file__).parent / ".tmp"
        tmp_dir.mkdir(exist_ok=True)
        combine_name = f"tmp_test_combined_example_{problem_id}.py"
        with open(tmp_dir / combine_name, "w") as f:
            combine(source, f.name)

            input_path = Path(__file__).parent / "input"
            stdin_paths = sorted(input_path.glob(f"{problem_id}*_in.txt"))
            stdout_paths = sorted(input_path.glob(f"{problem_id}*_out.txt"))

            for stdin_path, stdout_path in zip(stdin_paths, stdout_paths, strict=False):
                with open(stdin_path) as stdin:
                    output = run_example(f.name, stdin)

                with open(stdout_path) as stdout:
                    assert output == stdout.read()
