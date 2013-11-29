from StringIO import StringIO

from twisted.internet.defer import inlineCallbacks
from twisted.trial.unittest import TestCase as TrialTestCase

from verge import core


class TestMain(TrialTestCase):
    @inlineCallbacks
    def test_argument_appending(self):
        stdout = StringIO()
        yield core.run(
            arguments=["1", "2", "3"], command=["echo"], stdout=stdout,
        )
        self.assertEqual(
            sorted(stdout.getvalue().splitlines()), ["1", "2", "3"],
        )
