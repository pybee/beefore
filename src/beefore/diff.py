import os
import re

FILE_START = re.compile(r"diff --git a/(.*) b/(.*)")
LINE_RANGE = re.compile(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@")


def positions(directory, diff_content):
    """Given a diff payload, look for all the line ranges described for a given file.

    Returns a map of source file lines, mapped to the position in the diff
    that the line is referenced.
    """
    directory = os.path.abspath(directory)
    mappings = {}
    current_file = None
    file_start = None
    block_start = None
    block_offset = None
    for i, d in enumerate(diff_content):
        match = FILE_START.match(d)
        if match:
            current_file = {}
            filename = os.path.abspath(match.group(2))[len(directory)+1:]
            mappings[filename] = current_file

            # Start of a new file; so reset the file andd block offsets.
            file_start = None
            block_start = None
            block_offset = None
        elif current_file is not None:
            match = LINE_RANGE.match(d)
            if match:
                # Found the start of a new range in the file
                first_line = int(match.group(3))

                # If this is the first line range for a file,
                # then the line counter is also the starting index
                # for diff offsets.
                if file_start is None:
                    file_start = i

                block_start = i + 1
                block_offset = 1 if match.group(1) == '0' else 0
            elif block_start and len(d) > 0:
                if d[0] == '-':
                    block_offset += 1
                else:
                    current_file[i - block_start - block_offset + first_line] = i - file_start

    return mappings
