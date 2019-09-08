def unified_format(diff):
    udiff = diff.diff.decode("utf-8").splitlines()

    a_sha = diff.a_blob.hexsha[:7] if diff.a_blob else "0000000"
    b_sha = diff.b_blob.hexsha[:7] if diff.b_blob else "0000000"

    a_path = "{}".format(diff.a_path) if diff.a_path else "/dev/null"
    b_path = "{}".format(diff.b_path) if diff.b_path else "/dev/null"

    if diff.a_path is None:
        content = [
            "diff --git a/{a_path} b/{b_path}".format(a_path=b_path, b_path=b_path),
            "new file mode 100644",
            "index {a_sha}..{b_sha}".format(a_sha=a_sha, b_sha=b_sha),
            "--- {a_path}".format(a_path=a_path),
            "+++ b/{b_path}".format(b_path=b_path),
        ]
    elif diff.b_path is None:
        content = [
            "diff --git a/{a_path} b/{b_path}".format(a_path=a_path, b_path=a_path),
            "deleted file mode 100644",
            "index {a_sha}..{b_sha}".format(a_sha=a_sha, b_sha=b_sha),
            "--- a/{a_path}".format(a_path=a_path),
            "+++ {b_path}".format(b_path=b_path),
        ]
    else:
        content = [
            "diff --git a/{a_path} b/{b_path}".format(a_path=a_path, b_path=b_path),
            "index {a_sha}..{b_sha} 100644".format(a_sha=a_sha, b_sha=b_sha),
            "--- a/{a_path}".format(a_path=a_path),
            "+++ b/{b_path}".format(b_path=b_path),
        ]

    content.extend(udiff)

    return content


def full_diff(repository, branch="master"):
    content = []
    for diff in repository.commit(branch).tree.diff(None, create_patch=True):
        content.extend(unified_format(diff))
    return content


def check(check_module, directory, repository, branch, verbosity):
    print("Running %s check..." % check_module.__name__)
    print("==========" * 8)
    problems = check_module.check(
        directory=directory,
        diff_content=full_diff(repository, branch=branch),
        commit={"message": repository.commit().message},
        verbosity=verbosity,
    )
    print("==========" * 8)

    return not problems
