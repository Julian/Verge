from StringIO import StringIO
from unittest import TestCase

from verge import cli


class TestBasics(TestCase):
    def test_argument_appending(self):
        stdout = StringIO()

        def done():
            self.assertEqual(
                sorted(stdout.getvalue().splitlines()),
                ["1", "2", "3"],
            )

        return cli.main(
            arguments=["1", "2", "3"], command=["echo"], stdout=stdout
        ).addBoth(done)

