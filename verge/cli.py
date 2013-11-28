import argparse
import multiprocessing
import sys

from twisted.internet import defer, protocol, reactor
from twisted.internet.task import coiterate


class VergeProcess(protocol.ProcessProtocol):
    def __init__(self, stdout, stderr=sys.stderr, reactor=reactor):
        self.reactor = reactor
        self.stdout = stdout
        self.stderr = stderr

    @classmethod
    def spawn(cls, command, *args, **kwargs):
        process = cls(*args, **kwargs)
        process.reactor.spawnProcess(process, command[0], command, {})

    def errReceived(self, data):
        self.stderr.write(data)

    def outReceived(self, data):
        self.stdout.write(data)


def main(command, arguments=None, max_processes=None, stdout=sys.stdout):
    if arguments is None:
        arguments = sys.stdin
    if max_processes is None:
        max_processes = multiprocessing.cpu_count()

    processes = (
        VergeProcess.spawn(command + [argument.rstrip("\n")], stdout=stdout)
        for argument in arguments
    )

    deferreds = [coiterate(processes) for _ in xrange(max_processes)]
    return defer.gatherResults(deferreds)


parser = argparse.ArgumentParser()
parser.add_argument("command", nargs=argparse.REMAINDER)
