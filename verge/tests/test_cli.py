from StringIO import StringIO
from unittest import TestCase

from twisted.internet.defer import inlineCallbacks
from twisted.trial.unittest import TestCase as TrialTestCase

from verge import cli


class TestMain(TrialTestCase):
    @inlineCallbacks
    def test_argument_appending(self):
        stdout = StringIO()
        yield cli.main(
            arguments=["1", "2", "3"], command=["echo"], stdout=stdout,
        )
        self.assertEqual(
            sorted(stdout.getvalue().splitlines()), ["1", "2", "3"],
        )


class TestParseCLI(TestCase):
    def test_when_nothing_is_given_read_lines_from_stdin(self):
        stdin = StringIO("1\n2\n3\n")
        arguments = cli.parse(
            ["program", "arguments", "2", "program"],
            stdin=stdin,
        )
        arguments["arguments"] = list(arguments["arguments"])
        self.assertEqual(
            arguments, {
                "command": ["program", "arguments", "2", "program"],
                "arguments": ["1", "2", "3"],
            },
        )
