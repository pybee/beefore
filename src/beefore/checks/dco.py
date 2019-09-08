###########################################################################
# Check for the existence of a Developer Certificate of Origin
# in the commit.
###########################################################################

__name__ = "DCO"


class DCOProblem:
    def __str__(self):
        return "No DCO found"

    def add_comment(self, pull_request, commit, position):
        pull_request.create_comment(
            body="You haven't signed this pull request with a Developer "
            "Certificate of Origin (DCO). For details on what a DCO "
            "is, and what it means for your contribution, visit "
            "[this link](https://pybee.org/contributing/how/dco/)."
        )


def prepare(directory):
    pass


def check(directory, diff_content, commit, verbosity):
    expected_signoff = "\nSigned-off-by: "

    if expected_signoff in commit["message"]:
        print("DCO found.")
        return []

    print("No DCO found.")
    return [(DCOProblem(), None)]
