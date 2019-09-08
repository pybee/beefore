###########################################################################
# Check if any of the Python files touched by the commit have
# code style problems.
###########################################################################
import re
import subprocess

from beefore import diff

__name__ = 'Java CheckStyle'
LINT_OUTPUT = re.compile(r"\[checkstyle\] \[(ERROR)\] (.*?):(\d+):(?:\d+:)? (.*) \[(.*)\]")


class Lint:
    def __init__(self, filename, line, code, description):
        self.filename = filename
        self.line = line
        self.code = code
        self.description = description

    def __str__(self):
        return 'Line %s: [%s] %s' % (self.line, self.code, self.description)

    def add_comment(self, pull_request, commit, position):
        pull_request.create_review_comment(
            # body="At column %(col)d: [(%(code)s) %(description)s](http://.../%(code)s)" % {
            body="[%(code)s] %(description)s" % {
                'code': self.code,
                'description': self.description
            },
            commit_id=commit.sha,
            path=self.filename,
            position=position,
        )

    @staticmethod
    def find(directory):
        proc = subprocess.Popen(
            ['ant', 'checkstyle'],
            cwd=directory,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        out, err = proc.communicate()

        matches = LINT_OUTPUT.findall(err.decode('utf-8'))
        problems = {}
        for severity, filename, line, description, code in matches:
            problems.setdefault(filename, []).append(Lint(
                filename=filename,
                line=int(line),
                code=code,
                description=description,
            ))

        return problems


def prepare(directory):
    pass


def check(directory, diff_content, commit, verbosity):
    results = []

    lint_results = Lint.find(directory=directory)
    diff_mappings = diff.positions(directory, diff_content)

    for filename, problems in lint_results.items():
        file_seen = False
        if filename in diff_mappings:
            for problem in sorted(problems, key=lambda p: p.line):
                try:
                    position = diff_mappings[filename][problem.line]
                    if not file_seen:
                        print("  * %s" % filename)
                        file_seen = True
                    print('    - %s' % problem)
                    results.append((problem, position))
                except KeyError:
                    # Line doesn't exist in the diff; so we can ignore this problem
                    if verbosity:
                        if not file_seen:
                            print("  * %s" % filename)
                            file_seen = True
                        print('    - Line %s not in diff' % problem.line)
        else:
            # File has been changed, but wasn't in the diff
            if verbosity:
                if not file_seen:
                    print("  * %s" % filename)
                    file_seen = True
                print('    - file not in diff')

    return results
