import argparse
import sys


def parse(argv=None, stdin=sys.stdin):
    arguments = (line[:-1] for line in stdin)
    return dict(vars(parser.parse_args(argv)), arguments=arguments)


parser = argparse.ArgumentParser()
parser.add_argument("command", nargs=argparse.REMAINDER)
