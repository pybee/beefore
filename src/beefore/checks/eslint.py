###########################################################################
# Check if any of the Javascript files touched by the commit have
# code style problems.
###########################################################################
import json
import os.path
import re
import subprocess

import yaml

from beefore import diff

__name__ = 'ESLint'
LINT_OUTPUT = re.compile(r'(.*?): line (\d+), col (\d+), (.*?) - (.*) \((.*)\)')


class Lint:
    def __init__(self, filename, line, col, code, description):
        self.filename = filename
        self.line = line
        self.col = col
        self.code = code
        self.description = description

    def __str__(self):
        return 'Line %s, col %s: [%s] %s' % (self.line, self.col, self.code, self.description)

    def add_comment(self, pull_request, commit, position):
        pull_request.create_review_comment(
            body="At column %(col)d: [(%(code)s) %(description)s](http://eslint.org/docs/rules/%(code)s)" % {
                'col': self.col,
                'code': self.code,
                'description': self.description
            },
            commit_id=commit.sha,
            path=self.filename,
            position=position,
        )

    @staticmethod
    def find(directory):
        directory = os.path.abspath(directory)
        proc = subprocess.Popen(
            [
                'npx',
                'eslint',
                '--format', 'compact',
                '.',
            ],
            cwd=directory,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        out, err = proc.communicate()

        matches = LINT_OUTPUT.findall(out.decode('utf-8'))
        problems = {}
        for fname, line, col, level, description, code in matches:
            filename = os.path.abspath(fname)[len(directory)+1:]
            problems.setdefault(filename, []).append(Lint(
                filename=filename,
                line=int(line),
                col=int(col),
                code=code,
                description=description,
            ))

        return problems


SIMPLE_COMMENT = re.compile(r'//.*')
MULTILINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
SYMBOL_TO_STRING = re.compile(r'([a-zA-Z_][-\w_]*)\s*:')


def clean_json(raw):
    # Replace  //-style comments
    clean = SIMPLE_COMMENT.sub('', raw)

    # Replace  /* */-style comments
    clean = MULTILINE_COMMENT.sub('', clean)

    # Replace unadorned foo: 42 with "foo": 42
    clean = SYMBOL_TO_STRING.sub('"\\1":', clean)
    return clean


def install_eslint_config(directory):
    if os.path.isfile(os.path.join(directory, '.eslintrc')):
        with open(os.path.join(directory, '.eslintrc')) as config_file:
            config = json.loads(clean_json(config_file.read()))
    elif os.path.isfile(os.path.join(directory, '.eslintrc.json')):
        with open(os.path.join(directory, '.eslintrc.json')) as config_file:
            config = json.loads(clean_json(config_file.read()))
    elif os.path.isfile(os.path.join(directory, '.eslintrc.yml')):
        with open(os.path.join(directory, '.eslintrc.yml')) as config_file:
            config = yaml.load(config_file.read())
    else:
        config_file = None

    if config_file is None:
        print("No ESLint configuration file found.")
    else:
        try:
            extends_name = config['extends']
            print("Installing base ESLint configuration 'eslint-config-%s'..." % extends_name)
            proc = subprocess.Popen(['npm', 'install', 'eslint-config-%s' % extends_name])
            proc.wait()
        except KeyError:
            print("No base ESLint configuration specified.")


def prepare(directory):
    install_eslint_config(directory)


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
