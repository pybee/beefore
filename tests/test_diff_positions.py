import unittest

from beefore import diff


class TestDiff(unittest.TestCase):
    def test_add_lines(self):
        diff_content = [
            "diff --git a/tests/path/to/testfile b/tests/path/to/testfile",
            "@@ -1,4 +1,6 @@",
            " 1",
            "+2",
            "+3",
            " 4",
            " 5",
            " 6",
        ]

        self.assertEqual(
            diff.positions("tests", diff_content),
            {"path/to/testfile": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}},
        )

    def test_subtract_lines(self):
        diff_content = [
            "diff --git a/tests/path/to/testfile b/tests/path/to/testfile",
            "@@ -1,6 +1,2 @@",
            " 1",
            "-2",
            "-3",
            " 4",
        ]

        self.assertEqual(
            diff.positions("tests", diff_content), {"path/to/testfile": {1: 1, 2: 4}}
        )

    def test_add_subtract(self):
        diff_content = [
            "diff --git a/tests/path/to/testfile b/tests/path/to/testfile",
            "index 5f4d692..5b05678 100644",
            "--- a/tests/path/to/testfile",
            "+++ b/tests/path/to/testfile",
            "@@ -2,0 +2,1 @@",
            " 1",
            "+2",
            " 3",
            "@@ -13,7 +14,4 @@",
            " 4",
            "-5",
            "-6",
            "+7",
            " 8",
            "-9",
            "+10",
        ]

        self.assertEqual(
            diff.positions("tests", diff_content),
            {"path/to/testfile": {2: 1, 3: 2, 4: 3, 14: 5, 15: 8, 16: 9, 17: 11}},
        )

    def test_no_diff(self):
        diff_content = ["1", "2", "3", "4"]

        self.assertEqual(diff.positions("tests", diff_content), {})

    def test_multi_file(self):
        diff_content = [
            "diff --git a/tests/path/to/testfile b/tests/path/to/testfile",
            "index 5f4d692..5b05678 100644",
            "--- a/tests/path/to/testfile",
            "+++ b/tests/path/to/testfile",
            "@@ -2,0 +2,1 @@",
            " 1",
            "+2",
            " 3",
            "@@ -13,7 +14,4 @@",
            " 4",
            "-5",
            "-6",
            "+7",
            " 8",
            "-9",
            "+10",
            "diff --git a/tests/path/to/secondfile b/tests/path/to/secondfile",
            "index 5f4d692..5b05678 100644",
            "--- a/tests/path/to/secondfile",
            "+++ b/tests/path/to/secondfile",
            "@@ -2,0 +2,1 @@",
            " 1",
            "+2",
            " 3",
            "@@ -13,7 +14,4 @@",
            " 4",
            "-5",
            "-6",
            "+7",
            " 8",
            "-9",
            "+10",
        ]

        self.assertEqual(
            diff.positions("tests", diff_content),
            {
                "path/to/testfile": {2: 1, 3: 2, 4: 3, 14: 5, 15: 8, 16: 9, 17: 11},
                "path/to/secondfile": {2: 1, 3: 2, 4: 3, 14: 5, 15: 8, 16: 9, 17: 11},
            },
        )
